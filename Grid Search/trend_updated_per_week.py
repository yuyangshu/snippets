import collections
import csv
import pickle
from datetime import datetime
import numpy
import matplotlib.pyplot
from sklearn import datasets, linear_model

import data_loader


boundary = 287
base_date = data_loader.get_date("1/1/2016")
with open("suburbs", "rb") as f:
    suburbs = pickle.load(f)

count = collections.defaultdict(int)
total = collections.defaultdict(float)

for item in data_loader.read_csv_file("2016"):
    if item[13] not in suburbs or item[17] in ("", "0"):
        continue
    
    date = (data_loader.get_date(item[16].split()[0]) - base_date).days
    total[date] += float(item[17])
    count[date] += 1

raw_trend = []
for item in sorted(total):
    raw_trend.append(total[item] / count[item])


# "prediction"
trend = raw_trend[:boundary]
model = linear_model.LinearRegression()
for date in range(boundary, 366):
    # train new model
    if date % 7 == 0 and date // 7 < 52:
        model.fit(numpy.array(range(date)).reshape(-1, 1), raw_trend[:date])
    
    # predict trend
    trend.append(model.predict([[date]])[0])

matplotlib.pyplot.plot(raw_trend, color="orangered")
matplotlib.pyplot.plot(trend, color="turquoise")
matplotlib.pyplot.show()
# matplotlib.pyplot.savefig("trend_overlaid")

with open ("trend", "wb") as f:
    pickle.dump(trend, f)
