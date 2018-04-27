import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ],
    columns=["State", "RegionName"]  )

    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''

    state = None
    state_towns = []

    with open('university_towns.txt') as file:
        for line in file:
            current_line = line[:-1]
            if current_line[-6:] == '[edit]':
                state = current_line[:-6]
                continue
            if '(' in line:
                town = current_line[:current_line.index('(')-1]
                state_towns.append([state,town])
            else:
                town = current_line
                state_towns.append([state,town])

    df = pd.DataFrame(state_towns, columns = ["State", "RegionName"])

    return df



def get_recession_start():
    '''Returns the year and quarter of the recession start time as a
    string value in a format such as 2005q3'''

    xls = pd.ExcelFile("gdplev.xls")
    gdp_data = xls.parse()

    # Cleaning data (Removing unwanted rows and columns)
    gdp_data = gdp_data.drop([0,1,2,3,4,5,6])
    gdp_data.columns = gdp_data.iloc[0]
    gdp_data = gdp_data.drop([4])
    gdp_data.columns = ['Year', 'GDP of current dollars', 'GDP of chained 2009 dollars', '', 'Quarter', 'GDP in billions of current dollars', 'GDP in billions of chained 2009 dollars', 'nan']
    gdp_data = gdp_data.drop(['Year', 'GDP of current dollars', 'GDP of chained 2009 dollars', '', 'GDP in billions of current dollars', 'nan'], axis=1)
    gdp_data = gdp_data.drop(gdp_data.index[:212])
    gdp_data = gdp_data.set_index('Quarter')

    # Getting the difference in GDP for each Quarter
    gdp = gdp_data.diff()

    # Storing recession quarters (2 consecutive quarters where chained 2009 GDP is decreasing)
    for i,quarter in enumerate(gdp.index):
        if((gdp.iloc[i]<0).bool() and (gdp.iloc[i+1]<0).bool()):
            return quarter
    return None



def get_recession_end():
    '''Returns the year and quarter of the recession end time as a
    string value in a format such as 2005q3'''

    xls = pd.ExcelFile("gdplev.xls")
    gdp_data = xls.parse()

    # Cleaning data (Removing unwanted rows and columns)
    gdp_data = gdp_data.drop([0,1,2,3,5,6])
    gdp_data.columns = gdp_data.iloc[0]
    gdp_data = gdp_data.drop([4])
    gdp_data.columns = ['Year', 'GDP of current dollars', 'GDP of chained 2009 dollars', '', 'Quarter', 'GDP in billions of current dollars', 'GDP in billions of chained 2009 dollars', 'nan']
    gdp_data = gdp_data.drop(['Year', 'GDP of current dollars', 'GDP of chained 2009 dollars', '', 'GDP in billions of current dollars','nan'], axis=1)
    gdp_data = gdp_data.drop(gdp_data.index[:212])
    gdp_data = gdp_data.set_index('Quarter')

    # Getting the difference in GDP for each Quarter
    gdp = gdp_data.diff()

    # Ending recession quarters (2 consecutive quarters where chained 2009 GDP is increasing after recession starts)
    for i,quarter in enumerate(gdp.index):
        if((gdp.iloc[i-3]<0).bool() and (gdp.iloc[i-2]<0).bool() and (gdp.iloc[i-1]>0).bool() and (gdp.iloc[i]>0).bool()):
            return quarter
    return None



def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a
    string value in a format such as 2005q3'''

    gdp_data = pd.read_excel("gdplev.xls",skiprows=7)
    #gdp_data = xls.parse()

    # Cleaning data (Removing unwanted rows and columns)
    gdp_data.columns = ['Year', 'GDP of current dollars', 'GDP of chained 2009 dollars', '', 'Quarter', 'GDP in billions of current dollars', 'GDP in billions of chained 2009 dollars', 'nan']
    gdp_data = gdp_data.drop(['Year', 'GDP of current dollars', 'GDP of chained 2009 dollars', '', 'GDP in billions of current dollars', 'nan'], axis=1)
    gdp_data = gdp_data.drop(gdp_data.index[:212])
    gdp_data = gdp_data.set_index('Quarter')

    # Getting the difference in GDP for each Quarter
    gdp = gdp_data.diff()

    # Get quarter with minimum GDP in recession
    flag = 0
    for i,quarter in enumerate(gdp.index):
        if(flag==1 and (gdp.iloc[i+1]>0).bool() and (gdp.iloc[i+2]>0).bool()):
            end_index = i+1
            break
        if(flag==0 and (gdp.iloc[i]<0).bool() and (gdp.iloc[i+1]<0).bool()):
            strt_index = i
            flag = 1
    recession_years = gdp_data.iloc[strt_index:end_index]
    idx = recession_years.idxmin()
    return idx[0]


    return idx[0]



def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.

    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''

    homes = pd.read_csv('City_Zhvi_AllHomes.csv')

    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming',
              'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah',
              'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia',
              'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii',
              'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona',
              'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas',
              'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri',
              'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana',
              'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida',
              'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico',
              'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire',
              'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

    # Replace State full name from above abbreviation to state name mapping
    homes["State"].replace(states, inplace = True)
    homes = homes.set_index(["State", "RegionName"])
    # Remove unwanted columns from dataframe
    homes = homes.iloc[:, 49:250]

    def quarters(col):

        if col.endswith(("01", "02", "03")):
            s = col[:4]+"q1"
        elif col.endswith(("04", "05", "06")):
            s = col[:4]+"q2"
        elif col.endswith(("07", "08", "09")):
            s = col[:4]+"q3"
        else:
            s = col[:4]+"q4"

        return s

    housing = homes.groupby(quarters, axis=1).mean()

    return housing



def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''

    housing = convert_housing_data_to_quarters()
    university_towns = get_list_of_university_towns()
    quarter_before_recession = get_recession_start()
    recession_bottom = get_recession_bottom()

    # Keep only 2 columns - price berfore recession and price for recession bottom
    housing = housing[[quarter_before_recession,recession_bottom]]

    # Calculate a new column -"Price Ratio" to store the price ratio of quarter before recession to recession bottom
    housing["price_ratio"] = housing[quarter_before_recession]/housing[recession_bottom]
    housing = housing.dropna()

    # Get a data frome of all university town's housing data
    university_housing = housing.merge(university_towns, how="inner", left_index=True, right_index=True)

    #Get a data frame of all non-university town's housing data
    non_university_housing = housing[~housing.index.isin(university_housing.index)]

    # Run a ttest between 2 data frames
    t_stat, p_value = ttest_ind(university_housing["price_ratio"], non_university_housing["price_ratio"])

    if p_value < 0.01:
        different = True
    else:
        different = False

    if t_stat < 0:
        better = "university town"
    else:
        better = "non-university town"

    return (different, p_value, better)



get_list_of_university_towns()
get_recession_start()
get_recession_end()
get_recession_bottom()
convert_housing_data_to_quarters()
run_ttest()
