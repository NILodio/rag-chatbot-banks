import io
import os
import uuid
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from prefect import flow, get_run_logger, task
from prefect_aws import S3Bucket
from utils import get_base_url

load_dotenv()

block_s3_bucket = os.getenv("PREFECT_BLOCK_S3_BUCKET")
s3_bucket = S3Bucket.load(block_s3_bucket)


@task
def fetch_urls_from_s3(file: str = "data/source.txt") -> list[str]:
    """Reads the content of a file from S3 and returns it as a list of strings."""
    logger = get_run_logger()
    logger.info(f"Reading file from S3: {file}")

    try:
        content = s3_bucket.read_path(file)
        logger.info(f"Successfully read {len(content)} bytes from S3.")
        content_str = content.decode("utf-8")
        return (
            content_str.splitlines()
        )  # Return a list of strings, each representing a line
    except Exception as e:
        logger.error(f"Error reading file from S3: {e}")
        return []


@task
def put_data_to_s3(data: bytes, s3_key: str) -> None:
    logger = get_run_logger()
    logger.info(f"Uploading data to S3: {s3_key}")
    file_obj = io.BytesIO(data)
    try:
        s3_bucket.upload_from_file_object(file_obj, s3_key)
        logger.info(f"Successfully uploaded data to s3://{block_s3_bucket}/{s3_key}")
    except Exception as e:
        logger.error(f"Error uploading to S3: {e}")


@task
def get_pdf_urls(url):
    base_url = get_base_url(url)
    logger = get_run_logger()

    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching PDF URLs from {url}: {e}")
        return set()

    bs = BeautifulSoup(r.content, "html.parser")
    a_tags = bs.findAll("a")

    hrefs = [
        tag.attrs["href"]
        for tag in a_tags
        if "href" in tag.attrs.keys() and tag.attrs["href"].endswith(".pdf")
    ]

    return {href if href.startswith("http") else base_url + href for href in hrefs}


@task
def get_urls(url):
    base_url = get_base_url(url)
    logger = get_run_logger()

    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error requesting URL {url}: {e}")
        return set()

    bs = BeautifulSoup(r.content, "html.parser")
    a_tags = bs.findAll("a")

    hrefs = {tag.attrs["href"] for tag in a_tags if "href" in tag.attrs.keys()}
    hrefs = {href if href.startswith("http") else base_url + href for href in hrefs}

    return {
        href
        for href in hrefs
        if href.startswith(base_url) and not href.endswith(".pdf")
    }


@task
def download_pdf(pdf_url, save_path):
    logger = get_run_logger()
    original_filename = os.path.basename(pdf_url).split("/")[-1]
    rand_num = str(uuid.uuid4())
    new_filename = original_filename[:-4] + "_" + rand_num + original_filename[-4:]
    file = Path(new_filename)
    try:
        logger.info(f"Downloading PDF: {pdf_url}")
        r = requests.get(pdf_url, stream=True)
        r.raise_for_status()
        put_data_to_s3(r.content, f"{save_path}/{new_filename}")
        logger.info(f"Successfully uploaded PDF to S3: {file}")
    except requests.RequestException as e:
        logger.error(f"Error downloading PDF {pdf_url}: {e}")


@task
def download_pdfs(urls, save_path):
    logger = get_run_logger()
    logger.info(f"Starting download of {len(urls)} PDFs.")

    # Submit all download tasks concurrently
    download_tasks = [download_pdf.submit(url, save_path) for url in urls]

    for download_task in download_tasks:
        download_task.result()


@flow
def download_pdfs_from_url_recursive(
    url, save_path, remaining_levels, original_levels, unique_pdfs
):
    logger = get_run_logger()
    pdf_urls = get_pdf_urls(url)
    pdf_urls = [f for f in pdf_urls if f not in unique_pdfs]
    unique_pdfs.update(pdf_urls)

    logger.info(
        f"Depth Level 0 (Main Source) -> {len(pdf_urls)} PDFs found -> "
        f"Source: {url}"
    )

    download_pdfs(pdf_urls, save_path)

    if remaining_levels == 0:
        return

    remaining_levels -= 1
    other_urls = get_urls(url)
    for i, url_inside in enumerate(other_urls):
        download_pdfs_from_url_recursive(
            url_inside,
            save_path,
            remaining_levels,
            original_levels,
            unique_pdfs,
        )
        depth_level = original_levels - remaining_levels
        logger.info(
            f"Depth Level {depth_level} -> {i + 1}/{len(other_urls)} URLs -> "
            f"Source: {url_inside}"
        )


@flow
def download_pdfs_from_source(source_path: str, save_path: str, levels: int) -> None:
    sources = fetch_urls_from_s3(file="data/source.txt")
    for i, link in enumerate(sources):
        logger = get_run_logger()
        logger.info(f"Extracting Main Source #{i+1}: {link}")
        download_pdfs_from_url_recursive(
            link,
            save_path,
            remaining_levels=levels,
            original_levels=levels,
            unique_pdfs=set(),
        )


if __name__ == "__main__":
    download_pdfs_from_source(source_path="data", save_path="data/raw", levels=0)
