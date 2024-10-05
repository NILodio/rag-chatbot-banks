from bs4 import BeautifulSoup
from pathlib import Path
import requests
import re
import os
import random
from prefect import flow, get_run_logger, task
import boto3
from io import BytesIO

def get_base_url(url):
    # Extract the base url: protocol, subdomain, and domain
    base_re = r'^.+?[^\/:](?=[?\/]|$)'
    return re.findall(base_re, url)[0]

@task
def get_pdf_urls(url):
    # Extract the base url: protocol, subdomain, and domain
    base_url = get_base_url(url)
    
    # Stop processing if the request wasn't successful
    try:
        r = requests.get(url)
    except:
        return set()
    
    if r.status_code != 200:
        return set()
    
    # Extract all a-tags from the website HTML
    bs = BeautifulSoup(r.content)
    a_tags =  bs.findAll('a')
    
    # Loop through the a-tags saving all href attributes that end with .pdf
    hrefs = []
    for tag in a_tags:
        if 'href' in tag.attrs.keys() and tag.attrs['href'].endswith('.pdf'):
            hrefs.append(tag.attrs['href'])
    
    # Convert all hrefs to URLs by adding the base URL if required
    return {href if href.startswith('http') else base_url + href for href in hrefs}

@task
def get_urls(url):
    # Extract the base url: protocol + subdomain + domain
    base_url = get_base_url(url)
    
    # Stop processing if the request wasn't successful
    try:
        r = requests.get(url)
    except:
        logger = get_run_logger()
        logger.info("Error requesting URL... " + url)
        return
    if r.status_code != 200:
        return set()
    
    # Extract all a-tags from the website HTML
    bs = BeautifulSoup(r.content)
    a_tags =  bs.findAll('a')
    
    # Extract content of href attribute from the a-tags and convert them into proper URLs using the base url
    hrefs = {tag.attrs['href'] for tag in a_tags if 'href' in tag.attrs.keys()}
    hrefs = {href if href.startswith('http') else base_url + href for href in hrefs}
    
    # Return only URLs that don't end with .pdf and that start with the base URL
    return {href for href in hrefs if href.startswith(base_url) and not href.endswith('.pdf')}

@task
def download_pdfs(bucket_name,urls, save_path, print_details=False):
    client = boto3.client('s3')
    # Create/Save path where to store all PDFs
    path = Path(save_path)
    path.mkdir(parents=True, exist_ok=True)
    
    # Loop through the set of PDF URLs, get their contents and save the files
    for i, pdf_url in enumerate(urls):

        # Extract the original file name from the PDF in the website
        original_filename = os.path.basename(pdf_url).split('/')[-1]

        # Set up a new name by appending a random number to the original name (this avoids name duplication)
        rand_num = str(random.randrange(100000,199999))
        new_filename = original_filename[:-4] + '_' + rand_num + original_filename[-4:]

        # Start downloading the PDF, stop processing if the request wasn't successful
        logger = get_run_logger()
        if print_details:
            logger.info(f"Downloading ({i+1}/{len(urls)}) PDF... ")
        try:
            r = requests.get(pdf_url, stream=True)
        except:
            logger.info("Error downloading PDF... " + pdf_url)
            continue
        if r.status_code != 200:
            continue
        
        # If the file content was retrieved successfully, then write & save the new PDF file
        client.upload_fileobj(r.raw,bucket_name,save_path+'/'+new_filename)
        if print_details:
            logger.info("Successful... " + new_filename)

@flow
def download_pdfs_from_url_recursive(url, bucket_name,save_path, remaining_levels, original_levels, unique_pdfs, print_details=False):
    # Get all PDF URLs and work only with the ones not previously found
    pdf_urls = get_pdf_urls(url)
    pdf_urls = [f for f in pdf_urls if f not in unique_pdfs]
    unique_pdfs.update(pdf_urls)
    
    # Print PDFs found in the main source
    logger = get_run_logger()
    if remaining_levels == original_levels and print_details:
        logger.info( f"Depth Level 0 (Main Source) -> {len(pdf_urls)} PDFs found -> Source: {url}")
    
    # Download PDFs
    download_pdfs(bucket_name,pdf_urls, save_path, print_details)
    
    # If there's no remaining levels to dive, stop processing
    if remaining_levels == 0:
        return
    
    # Loop through the other URLs extracting PDF URLs from each one of them
    remaining_levels -= 1
    other_urls = get_urls(url)
    for i, url_inside in enumerate(other_urls):
        download_pdfs_from_url_recursive(url_inside, bucket_name,save_path, remaining_levels, original_levels, unique_pdfs, print_details)
        depth_level = original_levels - remaining_levels
        if print_details:
            logger.info("..." * (depth_level-1) + f"Depth Level {depth_level} -> {i + 1}/{len(other_urls)} URLs -> Source: {url_inside}")

@flow
def download_pdfs_from_source_txt(bucket_name:str,source_path:str,save_path:str,levels:int,print_details:bool):
    # INIIALIZE S3 CLIENT ######################
    client = boto3.client('s3')
    #####################################

    if source_path.startswith('http'):
        download_pdfs_from_url_recursive(source_path,bucket_name, save_path, remaining_levels=levels, original_levels=levels, unique_pdfs=set(), print_details=print_details)
    else:
        # Reading file form S3 Bucket
        response = client.get_object(Bucket = bucket_name, Key = source_path )
        data = response['Body'].read()
        
            # Use BytesIO to handle the bytes
        with BytesIO(data) as bio:
            # Decode bytes to string
            content = bio.getvalue().decode('utf-8')  # Decode bytes to string
            
            # Split the content into lines (links)
            links = content.splitlines()

        # Loop through the URLs, downloading the pdfs >=0 levels deep
        for i, line in enumerate(links):
            link = line.strip()
            
            # Print details if required
            if print_details:
                logger = get_run_logger()
                logger.info(f"Extracting Main Source #{i+1}: {link}")

            # Download all PDF files from each URL >=0 levels deep, into a specific folder for this URL only
            source_save_path = Path(save_path, str(i+1))
            download_pdfs_from_url_recursive(link, bucket_name,source_save_path, remaining_levels=levels, original_levels=levels, unique_pdfs=set(), print_details=print_details)
        

if __name__ == "__main__":
    pass