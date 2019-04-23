import collections
import csv
import time
import pickle
from datetime import datetime
import numpy
from scipy import spatial


# p 12 of https://www.pwc.com.au/consulting/assets/publications/big-city-analytics-apr15.pdf
economic_centres = [numpy.array((-33.870769, 151.206988)), # CBD
                    numpy.array((-33.814918, 151.000772)), # Parramatta
                    numpy.array((-33.835437, 151.207611)), # North Sydney
                    numpy.array((-33.780091, 151.115997))] # Macquarie Park

def read_csv_file(fname):
    with open(fname + ".csv", encoding="utf-8-sig", errors='ignore') as csvfile:
        reader = csv.reader((x.replace('\0', '') for x in csvfile), delimiter=',') # dialect = "excel"
        return list(reader)

def distance(coordinates, kdtree):
    return kdtree.query([coordinates], 1)[0][0]

def get_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%y")
    except:
        return datetime.strptime(date_str, "%d/%m/%Y")

def get_postcode(postcode):
    try:
        return int(postcode)
    except:
        return 0

def distance_to_entities(coordinates):
    return distance(coordinates, station_tree), distance(coordinates, hospital_tree), distance(coordinates, school_tree)

def distance_to_economic_centres(coordinates):
    def bind_coordinate(coordinates):
        def distance(eco_centre):
            return numpy.linalg.norm(eco_centre - coordinates)
        return distance

    return map(bind_coordinate(coordinates), economic_centres)

def get_job_data(coordinates):
    closest = tuple(job_map.data[job_map.query([coordinates], 1)[1][0]])
    return job_lookup_table[closest]

def extract_fields(item, date):
    def cast_and_mark_missing_values(x):
        return int(x) if x != "" else numpy.NaN

    coordinates = (float(item[73]), float(item[74]))
    return [cast_and_mark_missing_values(item[32]), # [0] area size
            cast_and_mark_missing_values(item[33]), # [1] number of bedrooms
            cast_and_mark_missing_values(item[34]), # [2] number of bathrooms
            cast_and_mark_missing_values(item[35]), # [3] number of parkings
            date, # [4] number of days since base date
            True if item[1] == "House" else False, # [5] is house or not
            *distance_to_entities(coordinates), # [6, 7, 8] distances to nearest train station, hospital, and high school
            *distance_to_economic_centres(coordinates), # [9, 10, 11, 12] distances to economic centres
            *get_job_data(coordinates), # [13, 14, 15, 16] number of industry, population, knowledge, and health jobs
            *coordinates, # [17, 18] latitude, longitude
            item[13], # [19] suburb
            get_postcode(item[14]), # [20] postcode
            float(item[17])] # [21] price


def load_data(house_only=False, verbose=False):

    print("starting to load data")
    timer_base = time.time()

    global station_tree
    with open("stations", "rb") as f:
        station_tree = spatial.KDTree(pickle.load(f))
    global hospital_tree
    with open("hospitals", "rb") as f:
        hospital_tree = spatial.KDTree(pickle.load(f))
    global school_tree
    with open("high_schools", "rb") as f:
        school_tree = spatial.KDTree(pickle.load(f))
    global suburbs
    with open("suburbs", "rb") as f:
        suburbs = pickle.load(f)
    global trend
    with open("trend", "rb") as f:
        trend = pickle.load(f)
    global job_map, job_lookup_table
    job_lookup_table = dict()
    with open("jobs", "rb") as f:
        job_lookup_table = pickle.load(f)
        job_map = spatial.KDTree(list(job_lookup_table.keys()))


    data = read_csv_file("2016")

    if verbose:
        print(f"finished reading csv files, {round(time.time() - timer_base)} seconds elapsed")

    base_date = get_date("1/1/2016")

    training_data, test_data = [], []
    boundary = 287  # floor(366 / 7 * 0.8) = 41, 41 * 7 = 287

    for item in data[1:]:
        # make sure the property is in sydney, has a lat/long pair, and a price
        if item[13] not in suburbs or item[73] == "" or item[17] in ("", "0"):
            continue

        date = (get_date(item[16].split()[0]) - base_date).days

        if house_only and item[1] != "House":
            continue

        if date < boundary:
            training_data.append(extract_fields(item, date))
        else:
            test_data.append(extract_fields(item, date))

    print(f"data loaded in {round(time.time() - timer_base)} seconds")

    return training_data, test_data