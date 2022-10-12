"""
Script to scrape postcoeds in VIC from postcodes-australia.com
Working as of 03-09-2022
"""

# built-in imports
import requests
from bs4 import BeautifulSoup


link = 'https://postcodes-australia.com/state-postcodes/vic'
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
postcode_list = []


bs = BeautifulSoup(requests.get(link, headers=headers).text, "html.parser")

# Slice list for postcodes only
a_list = bs.findAll("a")[34:-6]

for i in range(len(a_list)):
    a_list[i] = a_list[i].text

# Write postcodes to text file
with open('../data/raw/postcodes.txt', 'w') as f:
    for line in a_list:
        f.write(f"{line}\n")