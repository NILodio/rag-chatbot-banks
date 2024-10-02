from bs4 import BeautifulSoup
from pathlib import Path
import requests
import re
import os
import random
import prefect
from prefect import flow, get_run_logger, task


@flow
def get_base_url():
    url = "https://www.td.com/ca/en/about-td/for-investors/investor-relations/financial-information/financial-reports/quarterly-results"
    # Extract the base url: protocol, subdomain, and domain
    base_re = r'^.+?[^\/:](?=[?\/]|$)'
    base_url = re.findall(base_re, url)[0]
    logger = get_run_logger()
    logger.info("BASE_URL = %s", base_url)
    # return re.findall(base_re, url)[0]


# if __name__ == "__main__":
#     pass
