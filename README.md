# Generic Real Estate Consulting Project

Group 18 Members: Lucy (Yunfei) Liu (1142341), Xiran (Aran) Wang (1170876), Dustin Edgar Tano (1188678), Jane Vieren Anggani (1148126), Benedict Haryono (1166433)

This is our Final Industry Project for subject MAST30024 Applied Data Science at the University of Melbourne. In this project, we aim to:
1. Discover the **most significant internal and external features** for predicting rental prices in various SA2 suburbs within Victoria
2. Find suburbs with *highest predicted rental growth rate* within the next three years
3. Find the most *liveable* and *affordable* suburbs according to our chosen metrics

Ultimately we endeavor to provide data driven insights and guidance to real estate agencies who are looking to increase demand of their listed rental properties and maximise profit during this period of high uncertainty

**In order to run the code pipeline we have developed as part of this project, please follow the below steps:** 

1. Go to our data repository on google drive: https://drive.google.com/drive/folders/1Y3k7ujNOIbSrIAlJIWHFlnuAioTxkzK_?usp=sharing, and download the POIs, raw, and 2 shapefiles (LGA and SA2 shapefiles).

2. After cloning the repository onto a local, drag the zip files into `./data` (For the POIs files, it may be split into two when zipped, please make sure all zip files are in the folder to allow code to run smoothly)

3. Set directory to `./notebooks`

4. Download required packages from `requirements.txt`

5. Run  `notebooks/run.ipynb `


`run.ipynb` will automatically run the following notebooks in order: 

1. `Preprocess_domain_data.ipynb` - this notebooks preprocesses the scraped domain data to generate our main rental dataset 

2. `Preprocessing_population.ipynb`  - preprocesses population in each SA2 data taken from Australian Bureau of Statistics
Link to data source:abs.gov.au/statistics/people/population/regional-population-age-and-sex/latest-release

3. `Preprocess_income.ipynb` - preprocesses income from 2015 - 2019 - Data from Aurin:
https://data.aurin.org.au/dataset/au-govt-abs-abs-data-by-region-pop-and-people-asgs-sa3-2011-2019-sa3-2016

4. `Shapefiles_preprocessing.ipynb` - preprocesses LGA and SA2 shapefiles to be used in geoplots

Shapefiles for Local Government Area and Statistical taken from:https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files

5. `Crime_rate_preprocessing.ipynb` - preprocesses LGA crime rates and converts into ratios
Crime data from Crime Statistics Victoria: https://www.crimestatistics.vic.gov.au/crime-statistics/latest-crime-data-by-area

6. `Age_group_preprocessing.ipynb` - preprocesses population binned by age groups

7. `Crime_forecast_generation.ipynb` - creates future forecasts for crime rates based on current data

8. `Rental_data_analysis.ipynb` - analyses rental data (internal features)

9. `bbox_maker.ipynb` - Creates a bounding box for each property coordinate

10. `LGA_to_SA2_conversion.ipynb` - finds the SA2 regions within each LGA

11. `poi_analysis.ipynb` - analysis Points of interest (POIs)

12. `poi_dict_to_df.ipynb` - converts POIs data into a usable format

13. `Population_and_rent_geoplot.ipynb` - geoplots to visulise the SA2s and rental and population info

14. `Income_analysis.ipynb` - preliminary analysis of income data

15. `Income_forecast.ipynb` - creates futuristic income forecasts from past trends in income

16. `Merge_all_data.ipynb` - merge all external datasets into one for modelling and predictions

17. `Summary_notebook_skeleton.ipynb` - skeleton code for all the modelling and analysis conducted (feature selection, forecasts, liveability etc.)

18. `Summary_notebook_final.ipynb` - this is the official summary notebook to be presented to stakeholders to show all of our findings in the most interactive and readable format

**NOTE: The data from the POIs folder and rental data were scraped during mid-september 2022 and that is the data we used for this project. In order to reproduce the scraping process that we conducted to generate these datasets, please run the following notebooks:**

*Rental scraping process*
1. `postcode_scrape.ipynb` - Scrapes a list of postcodes in Victoria

2. `domain_scrape.ipynb` - Uses results from `postcode_scrape.ipynb` to scrape rental listings from domain.com.au

*OpenRouteService query process for POIs*

**You will need to apply for your own API keys**
1. `distance_to_cbd.ipynb` - queries driving distance and duration to CBD for each property from ORS API

2. `distance_json_to_csv.ipynb` - converts distance data from .json to .csv format

3. `poi_search.ipynb` - Queries for all POIs for each property from ORS API
