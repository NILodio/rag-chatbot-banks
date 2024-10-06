import os
import uuid
from datetime import timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from prefect import flow, get_run_logger, task
from prefect.tasks import task_input_hash
from prefect_aws import AwsCredentials, S3Bucket
from utils import get_base_url

load_dotenv()

block_s3_bucket = os.getenv("PREFECT_BLOCK_S3_BUCKET")
s3_bucket_name = os.getenv("AWS_BUCKET_NAME")

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.getenv("AWS_SESSION_TOKEN")
region_name = os.getenv("AWS_REGION")
block_name_aws = os.getenv("PREFECT_BLOCK_AWS_CREDENTIALS")
aws_credentials_block = AwsCredentials.load(block_name_aws)


s3_bucket = S3Bucket.load(block_s3_bucket)


@task
def fetch_urls_from_s3(path_s3: str, path: str, file: str = "url.txt") -> list[str]:
    s3_bucket.download_object_to_path(path_s3, os.path.join(path, file))
    with open(os.path.join(path, file)) as f:
        return list(map(str.strip, f.readlines()))


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def get_urls(url):
    # Extract the base url: protocol + subdomain + domain
    base_url = get_base_url(url)

    # Stop processing if the request wasn't successful
    try:
        r = requests.get(url)
    except requests.RequestException:
        logger = get_run_logger()
        logger.info("Error requesting URL... " + url)
        return
    if r.status_code != 200:
        return set()

    # Extract all a-tags from the website HTML
    bs = BeautifulSoup(r.content)
    a_tags = bs.findAll("a")

    # Extract content of href attribute from the a-tags
    # and convert them into proper URLs using the base url
    hrefs = {tag.attrs["href"] for tag in a_tags if "href" in tag.attrs.keys()}
    hrefs = {href if href.startswith("http") else base_url + href for href in hrefs}

    # Return only URLs that don't end with .pdf and that start with the base URL
    return {
        href
        for href in hrefs
        if href.startswith(base_url) and not href.endswith(".pdf")
    }


@task
def get_pdfs(urls, save_path, print_details=False):
    # Create/Save path where to store all PDFs
    path = Path(save_path)
    path.mkdir(parents=True, exist_ok=True)

    # Loop through the set of PDF URLs, get their contents and save the files
    for i, pdf_url in enumerate(urls):

        # Extract the original file name from the PDF in the website
        original_filename = os.path.basename(pdf_url).split("/")[-1]

        rand_num = str(uuid.uuid4())
        new_filename = original_filename[:-4] + "_" + rand_num + original_filename[-4:]
        file = Path(new_filename)

        logger = get_run_logger()
        if print_details:
            logger.info(f"Downloading ({i+1}/{len(urls)}) PDF... ")
        try:
            r = requests.get(pdf_url, stream=True)
        except requests.RequestException:
            logger.info("Error downloading PDF... " + pdf_url)
            continue
        if r.status_code != 200:
            continue

        # If the file content was retrieved successfully, then write & save the new PDF file
        with open(path.joinpath(file), "wb") as f:
            f.write(r.content)
        if print_details:
            logger.info("Successful... " + new_filename)


@flow
def download_pdfs(
    url, save_path, remaining_levels, original_levels, unique_pdfs, print_details=False
):
    # Get all PDF URLs and work only with the ones not previously found
    pdf_urls = get_urls(url)
    pdf_urls = [f for f in pdf_urls if f not in unique_pdfs]
    unique_pdfs.update(pdf_urls)

    logger = get_run_logger()
    if remaining_levels == original_levels and print_details:
        logger.info(
            f"Depth Level 0 (Main Source) -> {len(pdf_urls)} PDFs found -> "
            f"Source: {url}"
        )

    get_pdfs(pdf_urls, save_path)

    if remaining_levels == 0:
        return

    remaining_levels -= 1
    other_urls = get_urls(url)
    for i, url_inside in enumerate(other_urls):
        download_pdfs(
            url_inside,
            save_path,
            remaining_levels,
            original_levels,
            unique_pdfs,
            print_details,
        )
        depth_level = original_levels - remaining_levels
        if print_details:
            logger.info(
                "..." * (depth_level - 1)
                + f"Depth Level {depth_level} -> {i + 1}/{len(other_urls)} URLs -> "
                f"Source: {url_inside}"
            )


@flow
def get_data():
    source = fetch_urls_from_s3("data/source.txt", "data")
    save_path = "data"
    levels = 1
    print_details = True
    proper_save_path = Path(save_path)
    for i, link in enumerate(source):
        if print_details:
            logger = get_run_logger()
            logger.info(f"Extracting Main Source #{i+1}: {link.strip()}")
        source_save_path = Path(proper_save_path, str(i + 1))
        download_pdfs(
            link,
            source_save_path,
            remaining_levels=levels,
            original_levels=levels,
            unique_pdfs=set(),
            print_details=print_details,
        )


if __name__ == "__main__":
    get_data()
