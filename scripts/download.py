import requests
import os
import zipfile

'''
This script is used to download the required data files to ./data/raw.
The URLs for the files are located in ./scripts/file_download.txt,
and can be modified to suit the user's needs.
'''

urls = open("./file_download.txt").read().splitlines()

os.chdir("../data/raw")


for i in range(len(urls)):
    url = urls[i]
    file = requests.get(url)
    open(url.split("/")[-1], "wb").write(file.content)
    

os.mkdir('./SA2_Boundaries')

# Extract shapefile zipfile, courtesy of:
# https://stackoverflow.com/questions/3451111/unzipping-files-in-python
with zipfile.ZipFile('./SA2_2021_AUST_SHP_GDA2020.zip', 'r') as zip_ref:
    zip_ref.extractall('./SA2_Boundaries/')
    
# Delete original zip file
os.remove('./SA2_2021_AUST_SHP_GDA2020.zip')