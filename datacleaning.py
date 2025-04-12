# Script Opened: 4/12/25


#imports
import pandas as pd

#Path management
output_path = "/Users/pdeguz01/Documents/git/IDS705_TeamPandas/Output"

##################################
# Cleaning Los Angeles County Data

raw_lac = pd.read_csv("/Users/pdeguz01/Documents/git/Data/IDS705_Final/LACounty_Environmental_Health_Restaurant_and_Market_Inspections.csv", encoding="ISO-8859-1")

#drop unneeded columns
lac_colstokeep = ["ACTIVITY DATE", "FACILITY NAME", "FACILITY ADDRESS", "FACILITY CITY", "FACILITY ZIP", "SERVICE DESCRIPTION", "SCORE", "GRADE"]
lac_fewercols = raw_lac[lac_colstokeep]

#rename cols
lac_renamedict = {
    'ACTIVITY DATE': 'INSPECTION_DATE',
    'FACILITY NAME': 'STORE_NAME',
    'FACILITY ADDRESS': 'STREET_ADDRESS',
    'FACILITY CITY': 'CITY',
    'FACILITY ZIP': 'ZIP5',
    'SERVICE DESCRIPTION': 'SERVICE_DESCRIPTION',
    'SCORE': 'SCORE',
    'GRADE': 'GRADE'
}
lac_renamed = lac_fewercols.rename(columns=lac_renamedict)

#Clean dates
#convert "INSPECTION_DATE" to datetime
lac_renamed['INSPECTION_DATE'] = pd.to_datetime(
    lac_renamed['INSPECTION_DATE'].str.strip(),
    format='%m/%d/%Y'
)
#Creating new column with Year of Inspection Date
lac_renamed.loc[:,'INSPDATE_YEAR'] = lac_renamed['INSPECTION_DATE'].dt.year

#print(lac_renamed.columns.tolist())


##################################
#Cleaning Louisville, Kentucky Data


##################################
#Cleaning Austin TX data









##############################################
# Filtering data to just 2024 inspection dates

# Writing to Export