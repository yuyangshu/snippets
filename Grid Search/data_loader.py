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
    with open(fname + ".csv", encoding = "utf-8-sig", errors = 'ignore') as csvfile:
        reader = csv.reader((x.replace('\0', '') for x in csvfile), delimiter = ',') # dialect = "excel"
        return list(reader)

def distance(coordinates, kdtree):
    return kdtree.query([coordinates], 1)[0][0]

def get_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y%m%d")
    except:
        return datetime.strptime(date_str, "%d/%m/%Y")

def get_job_data(number_of_jobs):
    try:
        return int(number_of_jobs)
    except:
        return numpy.NaN

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

def extract_fields(item, date):
    def cast_and_mark_missing_values(x):
        return int(x) if x != "" else numpy.NaN

    coordinates = (float(item[77]), float(item[78]))
    return [cast_and_mark_missing_values(item[36]), # [0] area size
            cast_and_mark_missing_values(item[37]), # [1] number of bedrooms
            cast_and_mark_missing_values(item[38]), # [2] number of bathrooms
            cast_and_mark_missing_values(item[39]), # [3] number of parkings
            date, # [4] number of days since base date
            True if item[1] == "House" else False, # [5] is house or not
            *distance_to_entities(coordinates), # [6, 7, 8] distances to nearest train station, hospital, and high school
            *distance_to_economic_centres(coordinates), # [9, 10, 11, 12] distances to economic centres
            get_job_data(item[0]), # [13] industry jobs
            get_job_data(item[1]), # [14] population jobs
            get_job_data(item[2]), # [15] knowledge jobs
            get_job_data(item[3]), # [16] health jobs
            *coordinates, # [17, 18] latitude, longitude
            item[17], # [19] suburb
            get_postcode(item[18]), # [20] postcode
            float(item[21])] # [21] price

def extract_and_interpolate_fields(item):
    coordinates = (float(item[9]), float(item[8]))
    return [float(item[1]),
            int(item[2]),
            int(item[3]),
            2 if int(item[2]) > 2 else 1,
            (get_date("31/12/2036") - get_date("1/1/2016")).days,
            True if item[0] == "House" else False,
            *distance_to_economic_centres(coordinates),
            *distance_to_entities(coordinates),
            int(item[4]),
            int(item[5]),
            int(item[6]),
            int(item[7])]


def load_training_data(verbose = False):
    if verbose:
        print("starting to load data")
        timer_base = time.time()
        count = 0

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

    data = read_csv_file("scenario")
    if verbose:
        print(f"read {len(data)} entries from csv files,", round(time.time() - timer_base), "seconds elapsed") # 42

    base_date = get_date("1/1/2016")
    end_date = get_date("31/12/2016")

    selected_data = []
    prices = collections.defaultdict(list)

    for item in data[1:]:
        if item[17] not in suburbs or item[77] == "" or item[21] in ("", "0"):
            continue

        date = (get_date(item[20].split()[0]) - base_date).days
        if date < 0 or date > 365:  # 2016 is a leap year
            continue

        selected_data.append(extract_fields(item, date))
        prices[date].append(float(item[21]))

    if verbose:
        print(f"{len(selected_data)} entries extracted in {round(time.time() - timer_base)} seconds")

    trend = []
    for date in range(0, 366):
        trend.append(numpy.median(prices[date]))

    return selected_data, trend

def load_testing_data(filename):

    dummy_entities = __import__(filename)

    global station_tree
    with open("stations", "rb") as f:
        station_tree = spatial.KDTree(pickle.load(f) + dummy_entities.dummy_stations)
    global hospital_tree
    with open("hospitals", "rb") as f:
        hospital_tree = spatial.KDTree(pickle.load(f) + dummy_entities.dummy_hospitals)
    global school_tree
    with open("high_schools", "rb") as f:
        school_tree = spatial.KDTree(pickle.load(f) + dummy_entities.dummy_schools)
    global suburbs
    with open("suburbs", "rb") as f:
        suburbs = pickle.load(f)

    data = read_csv_file(filename)
    testing_data = [extract_and_interpolate_fields(item) for item in data[1:]]

    return testing_data
