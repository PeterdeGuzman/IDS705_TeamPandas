# Script Opened: 4/12/25


#imports
import pandas as pd
import re


##################################
#Custom Functions for cleaning addresses with regex

# Function to extract city from end of the string
def split_address(addr):
    for city in city_names:
        if addr.strip().endswith(city):
            street = addr[:addr.rfind(city)].strip()
            return pd.Series([street, city])
    return pd.Series([addr, None])  # fallback if no match


# Regex pattern for unit/suite/apartment/etc.
pattern = r'\b(?:Unit|UNIT|Bunit|Ste|STE|Suite|Apt|Bldg|Building|#)\s*[\w\-#]+$'

# Function to extract address line 2
def extract_address_line2(addr):
    addr = str(addr)  # Convert to string to avoid errors with NaN
    match = re.search(pattern, addr, re.IGNORECASE)
    if match:
        addr_line2 = match.group().strip()
        addr_main = addr.replace(match.group(), '').strip()
        return pd.Series([addr_main, addr_line2])
    else:
        return pd.Series([addr.strip(), None])




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

#cleaning addresses
lac_renamed[['STREET_ADDRESS', 'STREET_ADDRESS_LINE2']] = lac_renamed['STREET_ADDRESS'].apply(extract_address_line2)

#Clean dates
#convert "INSPECTION_DATE" to datetime
lac_renamed['INSPECTION_DATE'] = pd.to_datetime(
    lac_renamed['INSPECTION_DATE'].str.strip(),
    format='%m/%d/%Y'
)
#Creating new column with Year of Inspection Date
lac_renamed.loc[:,'INSPDATE_YEAR'] = lac_renamed['INSPECTION_DATE'].dt.year

# Adding State
lac_renamed["STATE"] = "CA"
#print(lac_renamed.columns.tolist())


##################################
#Cleaning Louisville, Kentucky Data

raw_lky = pd.read_csv("/Users/pdeguz01/Documents/git/Data/IDS705_Final/Louisville_Metro_KY_-_Restaurant_Inspection_Scores.csv")

# filter out schools and day cares?
#not sure if we should keep this column -- dropping for now
raw_lky['TypeDescription'].value_counts()

#drop unneeded columns
lky_colstokeep = ["Ins_TypeDesc", "EstablishmentName", "Address", "City", "State", "Zip", "InspectionDate", "score", "Grade"]
lky_fewercols = raw_lky[lky_colstokeep]

#rename cols
lky_renamedict = {
    'Ins_TypeDesc': 'SERVICE_DESCRIPTION',
    'InspectionDate': 'INSPECTION_DATE',
    'EstablishmentName': 'STORE_NAME',
    'Address': 'STREET_ADDRESS',
    'City': 'CITY',
    'Zip': 'ZIP5',
    'score': 'SCORE',
    'Grade': 'GRADE',
    'State': 'STATE'
}
lky_renamed = lky_fewercols.rename(columns=lky_renamedict)

#Clean dates
#convert "INSPECTION_DATE" to datetime
lky_renamed['INSPECTION_DATE'] = pd.to_datetime(
    lky_renamed['INSPECTION_DATE'],
    format='%Y/%m/%d %H:%M:%S'
)
#Creating new column with Year of Inspection Date
lky_renamed.loc[:,'INSPDATE_YEAR'] = lky_renamed['INSPECTION_DATE'].dt.year

#Cleaning Street address to extract address line 2
lky_renamed[['STREET_ADDRESS', 'STREET_ADDRESS_LINE2']] = lky_renamed['STREET_ADDRESS'].apply(extract_address_line2)


##################################
#Cleaning Austin TX data

#load raw data
import pandas as pd
import re
raw_atx = pd.read_csv("/Users/pdeguz01/Documents/git/Data/IDS705_Final/Austin_Food_Establishment_Inspection_Scores_20250411.csv")

#keep certain cols
atx_colstokeep = ['Restaurant Name', 'Zip Code', 'Inspection Date', 'Score', 'Address','Process Description']
atx_fewercols = raw_atx[atx_colstokeep]

#rename cols
atx_renamedict = {
    'Inspection Date': 'INSPECTION_DATE',
    'Restaurant Name': 'STORE_NAME',
    'Address': 'STREET_ADDRESS',
    'Zip Code': 'ZIP5',
    'Process Description': 'SERVICE_DESCRIPTION',
    'Score': 'SCORE',
}
atx_renamed = atx_fewercols.rename(columns=atx_renamedict)

#clean INSPECTION_DATE
atx_renamed['INSPECTION_DATE'] = pd.to_datetime(
    atx_renamed['INSPECTION_DATE'],
    format='%m/%d/%Y'
)
#Creating new column with Year of Inspection Date
atx_renamed.loc[:,'INSPDATE_YEAR'] = atx_renamed['INSPECTION_DATE'].dt.year

#Need to clean "STREET_ADDRESS" into columns: "STREET_ADDRESS" and "CITY"

atx_citynames = ["AUSTIN", "BEE CAVE", "BUDA", "CREEDMOOR", "DRIPPING SPRINGS", 
                 "ELGIN", "LAGO VISTA", "LAKEWAY", "MANOR",
                 "PFLUGERVILLE", "ROLLINGWOOD", "ROUND ROCK",
                 "SUNSET VALLEY", "WEST LAKE HILLS"]


# Sort city names by word count descending to catch multi-word cities first
city_names = sorted(atx_citynames, key=lambda x: -len(x.split()))


# Apply to the column
atx_renamed[['STREET_ADDRESS', 'CITY']] = atx_renamed['STREET_ADDRESS'].apply(split_address)

print(atx_renamed[['STREET_ADDRESS', 'CITY']])

# Apply the function to extract street address line 2
atx_renamed[['STREET_ADDRESS', 'STREET_ADDRESS_LINE2']] = atx_renamed['STREET_ADDRESS'].apply(extract_address_line2)

print(atx_renamed)
atx_renamed["STATE"] = "TX"

##############################################
# Merging data


#reordering columns in dataframes
datasets = [lac_renamed, lky_renamed, atx_renamed]
shared_cols = ['INSPECTION_DATE', 'STORE_NAME', 'STREET_ADDRESS', 'CITY', 'STATE', 'ZIP5', 
               'SERVICE_DESCRIPTION', 'SCORE', 'GRADE', 'STREET_ADDRESS_LINE2', 'INSPDATE_YEAR']
# Reorder each DataFrame in place
for i in range(len(datasets)):
    df = datasets[i]
    shared = [col for col in shared_cols if col in df.columns]
    others = [col for col in df.columns if col not in shared_cols]
    datasets[i] = df[shared + others]

combined_df = pd.concat([lac_renamed, lky_renamed, atx_renamed], ignore_index=True, sort=False)

##############################################
# Filtering data to just 2024 inspection dates

combined_df2024 = combined_df[combined_df["INSPDATE_YEAR"] == 2024]

# Writing to Export
#Path management
output_path = "/Users/pdeguz01/Documents/git/IDS705_TeamPandas/Output/healthinspections_2024.csv"
combined_df2024.to_csv(output_path, index=False)