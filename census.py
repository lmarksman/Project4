import requests
from config import CENSUS_API_KEY


'''
 Get FIPS information from FCC
 '''
def get_fips_information(latitude, longitude):
    params = {
        "format": "json",
        "showall": "true",
        "censusYear": "2010",
        "latitude": latitude,
        "longitude": -longitude
    }

    base_url = "https://geo.fcc.gov/api/census/block/find"

    response = requests.get(base_url, params=params)

    fcc_data = response.json()

    # print(fcc_data)

    l = {}

    l["state_code"] = fcc_data["State"]["FIPS"];
    l["county_code"] = fcc_data["County"]["FIPS"][2:5];
    l["tract_code"] = fcc_data["Block"]["FIPS"][5:11];

    return l

def get_income(l):
   
    income = "B19013_001E"
 
    get_vars = f'{income}'
 
    params = {
        "key": CENSUS_API_KEY,
        "get": get_vars,
        "for": "tract:" + l["tract_code"],
        "in": "state:" + l["state_code"] + "+county:" + l["county_code"]
    }
 
    base_ACS5 = "/2019/acs/acs5"
    base_url = "https://api.census.gov/data"
 
    response = requests.get(base_url + base_ACS5, params=params)
 
    census_data = response.json()
 
    a = census_data
 
    median_income = float(a[1][0])
 
    if median_income < 0:
        median_income = 0
 
    return median_income

# '''
# Get the income at a latitude/longitude in a census tract
# Uses FCC API to first turn latitude/longitude into a FIPS code then calls census for that FIPS code
# Census tracts contain between 2,500 to 8,000 people
# '''
# def income(latitude, longitude):
 
#     l = get_fips_information(latitude, longitude)
 
#     inc = get_income(l)
 
#     r = {
#         "Status": "Ok",
#         "income": inc
#     }
 
#     return r

def get_population_density(l):
    # Get census data based on FIPs code
    params = {
        "key": CENSUS_API_KEY,
        "get": "B17001_001E",
        "for": "tract:" + l["tract_code"],
        "in": "state:" + l["state_code"] + "+county:" + l["county_code"]
    }

    base_ACS5 = "/2019/acs/acs5"
    base_url = "https://api.census.gov/data"

    response = requests.get(base_url + base_ACS5, params=params)

    census_data = response.json()

    a = census_data
    population = float(a[1][0])

    params = {
        "key": CENSUS_API_KEY,
        "get": "LAND_AREA",
        "for": "tract:" + l["tract_code"],
        "in": "state:" + l["state_code"] + "+county:" + l["county_code"]
    }

    base_PDB  = "/2019/pdb/tract"
    base_url = "https://api.census.gov/data"

    response = requests.get(base_url + base_PDB, params=params)

    census_data = response.json()

    # square miles
    a = census_data
    land_area = float(a[1][0])

    #print(",".join(a[0]))
    #print(",".join(a[1]))

    if float(land_area) > 0.0:
        pop_density = population / land_area
    else:
        pop_density = 0.0

    return round(pop_density, 2)

# '''
# Get the population density at a latitude/longitude in a census tract
# Uses FCC API to first turn latitude/longitude into a FIPS code then calls census for that FIPS code
# Census tracts contain between 2,500 to 8,000 people
# '''
# def population_density(latitude, longitude):

#     l = get_fips_information(latitude, longitude)

#     pop_density = get_population_density(l)

#     r = {
#         "Status": "Ok",
#         "population_density": pop_density
#     }

#     return r



'''
Get a summary at a latitude/longitude in a census tract
Uses FCC API to first turn latitude/longitude into a FIPS code then calls census for that FIPS code
Census tracts contain between 2,500 to 8,000
'''
def summary(latitude,longitude):

    # print(latitude,longitude)
    try: 
        l = get_fips_information(latitude, -longitude)
    
        pop_density = get_population_density(l)
        income = get_income(l)
        
        r = {
            "Status": "Ok",
            "income": income,
            "population_density": pop_density
        }
    except:
        r = {
            "Status": "Error"
        }
        return r
    return r


