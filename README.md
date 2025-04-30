# IDS705 - Principles of Machine Learning Final Project
## Team Flamingo

Team Members:
- Leo Chen
- Peter de Guzman
- Dhivahari Vivek
- Jenny Wu

# Repository Description
This repository contains the code and select raw data that our team used to analyze the impact of neighborhood context on predicting restaurant health inspection scores. This README document contains a description of the repository's structure and contents. All dependencies for the data preprocessing, merging, analysis and reporting are listed in the `requirements.txt` file. 

Please reach out to the team members if you have any additional questions! 

# Folder Structure:


# PLEASE NOTE - Accessing the dataset
When conducting these analyses, many members of our team used the included `.gitignore` functionality, as intermediate merged files and notebooks were too large to be pushed to GitHub. In addition, our final merged and enriched dataset was too large to store on GitHub. It can instead be accessed through Duke Box. We have created a folder and invited Professor Bradbury to this folder to access the dataset. As a result, the hardcoded paths that are used to load in the merged dataset in our notebooks cannot run without being changed to path to this dataset. 
- Link to dataset https://duke.box.com/s/77n6pt1ehwze3vd5aexsprj979s01dpw

# Reproducing the dataset

1. The link to the three raw datasets can be found below. Using the Python code in `01-Data Processing Scripts/a-merging_restauranthealthinspections.ipynb`, the datasets from Los Angeles County, CA, Louisville, KY, and Austin, TX can be cleaned and merged. 
2. After merging the restaurant data, we sent it to the company Geocodio to geocode the dataset, appending latitude, longitude, and other geographic variables. Therefore, we don't have the code that geocoded that data, but the geocoded restaurant health inspections dataset can be found at the following path: "IDS705_TeamPandas/Data/Geocoded_Data/healthinspections_2024_geocoded.csv".
3. The notebook `01-Data Processing Scripts/b-merging_censusSVIUSDA.ipynb` contains the remainder of the dataset processing and merging code. This script creates a 1/2 mile buffer around each restaurant, and identifies the Census tracts that intersect with this buffer. Then, we download a list of variables from the 2023 5-Year American Community Survey dataset using the `censusdis` package. These variables are: `"MEDIAN_HOUSEHOLD_INCOME_VARIABLE", "AVG_HOUSEHOLD_SIZE", "TOTAL_POPULATION", "MEDIAN GROSS RENT"`. Grouping by restaurant and inspection date, we calculate the average value of each of these Census variables for each intersecting Census tract. Then we merge these back in to the restaurants dataset. Next, we merged in the Social Vulnerability Index data at the Census tract level. Finally, we merged in the USDA Food Access Research Atlas data at the Census tract level.
4. As mentioned above, this final merged dataset is too large to be pushed to GitHub, so we saved it to Duke Box. 

Link to raw datasets and helpful resources:
- Los Angeles County, California restaurant health inspections https://data.lacounty.gov/datasets/lacounty::environmental-health-restaurant-and-market-inspections-04-01-2022-to-03-31-2025/about
- Louisville, Kentucky metro area restaurant health inspections https://catalog.data.gov/dataset/louisville-metro-ky-restaurant-inspection-scores
- Austin, Texas restaurant health inspections https://data.austintexas.gov/Health-and-Community-Services/Food-Establishment-Inspection-Scores/ecmv-9xxi/about_data
- USDA ATSDR GRASP SVI Data & Documentation Download https://www.atsdr.cdc.gov/place-health/php/svi/svi-data-documentation-download.html
- USDA ERS Food Access Research Atlas Data & Documentation https://www.ers.usda.gov/data-products/food-access-research-atlas/download-the-data
- US Census Bureau Census tract shapefiles https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html 
- `censusdis` Python package documentation https://censusdis.readthedocs.io/en/v1.1.14/index.html
- Geocodio https://www.geocod.io/
