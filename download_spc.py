# coding: utf-8
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time 

atc_groups = {
        'A': 38, #38 pages on SUKL website
        'B': 33, #33 pages on SUKL website
        'C': 67, #67 pages on SUKL website
        }

urls = []

for atc, page_max in atc_groups.items():
    for i in range(1, page_max + 1):
        sukl =  f"http://www.sukl.cz/modules/medication/search.php"
        sukl += f"?data%5Batc_group%5D={atc}"
        sukl += f"&data%5Bchbox%5D%5B0%5D=marketability"
        sukl += f"&page={i}"

        r = requests.get(sukl)
        soup = BeautifulSoup(r.text)
        tds = soup.find_all('td', {'headers': 'spc'})
        a = [ td.find_all('a') for td in tds ]

        #filter blank spcs
        href_lists = list(filter( lambda l: l != [], a ))
        hrefs = [ a for a in href_lists ]
        hrefs = [ a[0]['href'] for a in hrefs ]
        urls.extend(hrefs)
        time.sleep(3)
unique_urls = set(urls)

for i, url in enumerate(unique_urls):
    print(url)
    filename = Path(f"spc/{i}.pdf")
    r = requests.get(url)
    filename.write_bytes(r.content)
    time.sleep(3)
