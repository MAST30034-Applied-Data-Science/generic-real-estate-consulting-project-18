"""
A very simple and basic web scraping script. Feel free to
use this as a source of inspiration, but, make sure to attribute
it if you do so.

This is by no means production code.
"""
# built-in imports
import re
import pandas as pd
from json import dump
from time import sleep
from datetime import date
import requests
import random

from collections import defaultdict

# user packages
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen

# constants
BASE_URL = "https://www.domain.com.au"
RENT_LINK1 = f'/rent/?postcode='
RENT_LINK2 = f'&sort=default-desc&page='
N_PAGES = range(1, 51)

headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

# Read in list of postcodes in VIC
file = open('../data/raw/postcodes.txt', 'r')
data = file.read()
postcodes = data.replace('\n', ' ').split(" ")
file.close()
postcodes = postcodes[:-1]


# begin code
url_links = []
property_metadata = defaultdict(dict)

# generate list of urls to visit
for code in postcodes:
    rent_url_incomplete = BASE_URL + RENT_LINK1 + code
    for page in N_PAGES:
        rent_url = rent_url_incomplete + RENT_LINK2 + str(page)
        
        bs_object_rent = BeautifulSoup(requests.get(
                                                    rent_url, 
                                                    headers=headers).text, 
                                                    "html.parser")
        

        # find all href (a) tags that are from the base_url website.
        index_links = bs_object_rent \
            .findAll(
                "a") # the `*` denotes wildcard any

        for link in index_links:
            # if its a property address, add it to the list
            if 'address' in link['class']:
                url_links.append(link['href'])
        
# Remove duplicate links
url_links = list(set(url_links))

# Save url list to text file for archiving
with open(f'../data/raw/urls{str(date.today())[4:]}.txt', 'w') as f:
    for line in url_links:
        f.write(f"{line}\n")


# for each url, scrape some basic metadata
for property_url in url_links:
    bs_object_rent = BeautifulSoup(requests.get(
                                                property_url, 
                                                headers=headers).text, 
                                                "html.parser")

    # looks for the header class to get property name
    try:
        property_metadata[property_url]['name'] = bs_object_rent \
            .find("h1", {"class": "css-164r41r"}) \
            .text
    except:
        property_metadata[property_url]['name'] = None

    # looks for the div containing a summary title for cost
    try:
        property_metadata[property_url]['cost_text'] = bs_object_rent \
            .find("div", {"data-testid": "listing-details__summary-title"}) \
            .text
    except:
        property_metadata[property_url]['cost_text'] = None

    # Find text for property type
    try:
        property_metadata[property_url]['property_type'] = bs_object_rent \
            .find("div", {"data-testid": "listing-summary-property-type"}) \
            .findAll("span", {"class": "css-in3yi3"})[0]
    except:
        property_metadata[property_url]['property_type'] = None
    
    # Record any additional information provided
    try:
        property_metadata[property_url]['extra'] = bs_object_rent \
            .find("ul", {"data-testid": "listing-summary-strip"})
    except:
        property_metadata[property_url]['extra'] = None
    
    # extract coordinates from the hyperlink provided
    try:
        property_metadata[property_url]['coordinates'] = [
            float(coord) for coord in re.findall(
                r'destination=([-\s,\d\.]+)', # use regex101.com here if you need to
                bs_object_rent \
                    .find(
                        "a",
                        {"target": "_blank", 'rel': "noopener noreferer"}
                    ) \
                    .attrs['href']
            )[0].split(',')
        ]
    except:
        property_metadata[property_url]['coordinates'] = None

    
    try:
        property_metadata[property_url]['rooms'] = [
            re.findall(r'\d\s[A-Za-z]+', feature.text) for feature in bs_object_rent \
                .find("div", {"data-testid": "property-features"}) \
                .findAll("span", {"data-testid": "property-features-text-container"})
        ]
    except:
        property_metadata[property_url]['rooms'] = None


    try:
        property_metadata[property_url]['desc_title'] = bs_object_rent \
            .findAll("h4", {"data-testid": "listing-details__description-headline"})
    except:
        property_metadata[property_url]['desc_title'] = None

    # Scrape property description
    try:
        property_metadata[property_url]['desc'] = bs_object_rent \
            .find("div", {"data-testid": "listing-details__description"}) \
            .findAll("p")
    except:
        property_metadata[property_url]['desc'] = None
    
    # Scrape neighbourhood demographics data
    try:
        property_metadata[property_url]['neighbourhood_insights'] = bs_object_rent \
            .findAll("tr", {"data-testid": "neighbourhood-insights__age-brackets-row"})
    except:
        property_metadata[property_url]['neighbourhood_insights'] = None

df = pd.DataFrame(property_metadata).transpose()


# output to datestamped csv file in data/raw/
df.to_csv(f'../data/raw/property_data_raw{str(date.today())[4:]}.csv')