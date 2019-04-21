import collections
import csv
import pickle
import numpy

with open("jobs.csv") as f:
    reader = csv.reader((x.replace('\0', '') for x in f), delimiter=',') # dialect = "excel"
    data = list(reader)[1:]

mapping = collections.defaultdict(list)
counter = 0
for row in data:
    if row[0] not in ("", "0") and row[77] != "":
        mapping[(int(row[0]), int(row[1]), int(row[2]), int(row[3]))].append((float(row[77]), float(row[78])))
        counter += 1

reverse_mapping = dict()
for key in mapping.keys():
    reverse_mapping[tuple(numpy.median(mapping[key], axis=0))] = key

# print(len(reverse_mapping), counter)
# 17600 1126175 (1.563%)

with open("jobs", "wb") as f:
    pickle.dump(reverse_mapping, f)