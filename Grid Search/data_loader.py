import collections
import csv
import time
from datetime import datetime

import numpy
from scipy import spatial
from sklearn import linear_model


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
            *distance_to_entities(coordinates), # [5, 6, 7] distance to nearest train station, hospital, and high school
            *get_job_data(coordinates), # [8, 9, 10] number of industry, population, knowledge, and health jobs
            *coordinates, # [11, 12] latitude, longitude
            item[13], # [13] suburb
            get_postcode(item[14]), # [14] postcode
            float(item[17])] # [15] price


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
    global job_map, job_lookup_table
    job_lookup_table = dict()
    with open("jobs", "rb") as f:
        job_lookup_table = pickle.load(f)
        job_map = spatial.KDTree(list(job_lookup_table.keys()))


    data = read_csv_file("1") + read_csv_file("2")[1:]
    if verbose:
        print(f"{len(data)} entries in 2001 to mid 2016")   # 2698727
    deduplication = set()
    for item in data[1:]:
        deduplication.add(item[0])

    for item in read_csv_file("2016")[1:]:
        if item[0] not in deduplication:
            data.append(item)
            deduplication.add(item[0])
    if verbose:
        print(f"{len(data)} entries in 2001 to 2016")       # 2785299
    
    data += read_csv_file("2017")[1:]
    if verbose:
        print(f"{len(data)} entries in 2001 to 2017")       # 2921280

    if verbose:
        print(f"finished reading csv files, {round(time.time() - timer_base)} seconds elapsed")

    base_date = get_date("1/1/2001")

    global trend
    boundary = (get_date("1/10/2017") - base_date).days     # 6117
    count = collections.defaultdict(int)
    total = collections.defaultdict(float)

    for item in data:
        if item[13] not in suburbs or item[73] == "" or item[17] in ("", "0"):
            continue
    
        date = (get_date(item[16].split()[0]) - base_date).days
        if date >= boundary:
            continue

        total[date] += float(item[17])
        count[date] += 1

    trend = []
    for date in range(boundary):
        if date in total:
            trend.append(total[date] / count[date])
        else:
            # only day with no data: 1089
            trend.append(trend[-1])

    model = linear_model.LinearRegression()
    model.fit(numpy.array(range(boundary)).reshape(-1, 1), trend)
    if verbose:
        print(f"model parameters: {model.coef_}, {model.intercept_}")
        # model parameters: [98.19991829], 392559.3697551081

    for date in range(boundary, (get_date("31/12/2017") - base_date).days + 1):
        trend.append(model.predict([[date]])[0])
    prediction_date = "18/6/2036"
    prediction_date_trend = model.predict([[(get_date(prediction_date) - base_date).days]])[0]
    if verbose:
        print(f"prediction date trend: {prediction_date_trend}")
        # prediction date trend: 1664444.71149635

    if verbose:
        print(f"finished computing trend, {round(time.time() - timer_base)} seconds elapsed")

    training_data, test_data = [], []
    counter = 0

    for item in data[1:]:
        # make sure the property is in sydney, has a lat/long pair, and a price
        if item[13] not in suburbs or item[73] == "" or item[17] in ("", "0"):
            continue

        date = (get_date(item[16].split()[0]) - base_date).days

        if house_only and item[1] != "House":
            continue

        counter += 1
        if counter % 100000 == 0:
            print(f"{counter} entries processed")

        if date < boundary:
            training_data.append(extract_fields(item, date))
        else:
            test_data.append(extract_fields(item, date))

    print(f"data loaded in {round(time.time() - timer_base)} seconds")

    # more than 1,700,000 but less than 1,800,000 entries in total
    return training_data, test_data, trend, prediction_date_trend
