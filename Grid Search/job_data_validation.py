import collections
import csv
import pickle
import numpy
from scipy import spatial


def get_job_data(coordinates):
    closest = tuple(job_map.data[job_map.query([coordinates], 1)[1][0]])
    return job_lookup_table[closest]

job_lookup_table = dict()
with open("jobs", "rb") as f:
    job_lookup_table = pickle.load(f)
    job_map = spatial.KDTree(list(job_lookup_table.keys()))

with open("jobs.csv") as f:
    reader = csv.reader((x.replace('\0', '') for x in f), delimiter=',') # dialect = "excel"
    data = list(reader)[1:]

agree = 0
disagree = 0

for row in data:
    if row[0] not in ("", "0") and row[77] != "":
        result = get_job_data((float(row[77]), float(row[78])))
        if result[0] != int(row[0]) or result[1] != int(row[1]) or result[2] != int(row[2]) or result[3] != int(row[3]):
            disagree += 1
        else:
            agree += 1

print(agree, disagree, agree / float(agree + disagree))
# 900988 225187 0.8000426221501987
# testing for each field independently yields similar results: 3605040 899660 0.8002841476679912