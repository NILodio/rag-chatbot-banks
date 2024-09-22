import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

url = "https://www.td.com/ca/en/about-td/for-investors/investor-relations/financial-information/financial-reports/quarterly-results"

folder_location = "data/pdf_files"
if not os.path.exists(folder_location):
    os.mkdir(folder_location)

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
for link in soup.select("a[href$='.pdf']"):
    filename = os.path.join(folder_location, link["href"].split("/")[-1])
    with open(filename, "wb") as f:
        f.write(requests.get(urljoin(url, link["href"])).content)
