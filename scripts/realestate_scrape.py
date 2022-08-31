"""
A very simple and basic web scraping script. Feel free to
use this as a source of inspiration, but, make sure to attribute
it if you do so.

This is by no means production code.
"""
# built-in imports
import re
from json import dump

from collections import defaultdict

# user packages
from bs4 import BeautifulSoup
from urllib.request import urlopen

# constants
BASE_URL = "https://www.realestate.com.au"
RENT_LINK = "/rent/in-vic/list-"
BUY_LINK = "/buy/in-vic/list-"
N_PAGES = range(1, 80) # update this to your liking

# begin code
url_links = []
property_metadata = defaultdict(dict)

# generate list of urls to visit
for page in N_PAGES:
    rent_url = BASE_URL + RENT_LINK + page
    buy_url = BASE_URL + BUY_LINK + page
    bs_object_rent = BeautifulSoup(urlopen(rent_url), "lxml")
    bs_object_buy = BeautifulSoup(urlopen(buy_url), "lxml")

    # find the unordered list (ul) elements which are the results, then
    # find all href (a) tags that are from the base_url website.
    index_links = bs_object_rent \
        .find(
            "ul",
            {"data-testid": "results"}
        ) \
        .findAll(
            "a",
            href=re.compile(f"{BASE_URL}/*") # the `*` denotes wildcard any
        )

    for link in index_links:
        # if its a property address, add it to the list
        if 'address' in link['class']:
            url_links.append(link['href'])


# for each url, scrape some basic metadata
for property_url in url_links[1:]:
    bs_object_rent = BeautifulSoup(urlopen(property_url), "lxml")

    # looks for the header class to get property name
    property_metadata[property_url]['name'] = bs_object_rent \
        .find("h1", {"class": "css-164r41r"}) \
        .text

    # looks for the div containing a summary title for cost
    property_metadata[property_url]['cost_text'] = bs_object_rent \
        .find("div", {"data-testid": "listing-details__summary-title"}) \
        .text

    # extract coordinates from the hyperlink provided
    # i'll let you figure out what this does :P
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

    property_metadata[property_url]['rooms'] = [
        re.findall(r'\d\s[A-Za-z]+', feature.text)[0] for feature in bs_object_rent \
            .find("div", {"data-testid": "property-features"}) \
            .findAll("span", {"data-testid": "property-features-text-container"})
    ]

    property_metadata[property_url]['desc'] = re \
        .sub(r'<br\/>', '\n', str(bs_object_rent.find("p"))) \
        .strip('</p>')

# output to example json in data/raw/
with open('../data/raw/example.json', 'w') as f:
    dump(property_metadata, f)