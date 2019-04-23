import os
import os.path
import collections
import time
import concurrent.futures
import pickle
import numpy
import xgboost
from scipy import spatial
from sklearn import preprocessing, metrics, model_selection, linear_model

import grid_loader


def run_parameter_set(X_train, Y_train, X_test, Y_test, num_rounds, eta, subsample, colsample, max_depth):
    print(f"executing num_rounds={num_rounds}, eta={eta}, sumsampling={subsample}, max_depth={max_depth}")

    with open("trend", "rb") as f:
        trend = pickle.load(f)

    # calculate training targets
    Y_train_target = []
    for index, entry in enumerate(Y_train):
        Y_train_target.append(entry - trend[X_train[index][4]])

    # train the model
    parameters = {"eta": eta,
                  "seed": 0,
                  "subsample": subsample,
                  "colsample_bytree": colsample,
                  "objective": "reg:linear",
                  "max_depth": max_depth,
                  "min_child_weight": 1,
                  "verbosity": 0}
    matrix = xgboost.DMatrix(X_train, Y_train_target)
    xgboost_model = xgboost.train(parameters, matrix, num_boost_round=num_rounds)

    # training percentage errors
    training_predictions = xgboost_model.predict(xgboost.DMatrix(X_train))
    for index, entry in enumerate(X_train):
        training_predictions[index] += trend[entry[4]]
    training_errors = (training_predictions - Y_train) / Y_train
    absolute_training_errors = numpy.absolute(training_errors)

    # testing percentage errors
    testing_predictions = xgboost_model.predict(xgboost.DMatrix(X_test))
    for index, entry in enumerate(X_test):
        testing_predictions[index] += trend[entry[4]]
    testing_errors = (testing_predictions - Y_test) / Y_test
    absolute_testing_errors = numpy.absolute(testing_errors)

    # return result
    return f"{num_rounds},{eta},{subsample},{max_depth},{numpy.mean(absolute_training_errors)},{numpy.median(absolute_training_errors)},{min(testing_errors)},{max(testing_errors)},{numpy.mean(absolute_testing_errors)},{numpy.median(absolute_testing_errors)},{numpy.std(absolute_testing_errors)}\n"

if __name__ == "__main__":
    # configs
    house_only = False
    dump_file_name = "scenario_hack_grid"
    timer_base = time.time()

    # load data
    if os.path.isfile(dump_file_name):
        with open(dump_file_name, "rb") as f:
            training_data = pickle.load(f)
            testing_data = pickle.load(f)
        print(f"loaded dumped data, {round(time.time() - timer_base)} seconds elapsed")
    else:
        training_data, testing_data = grid_loader.load_data(house_only=house_only, verbose=False)
        with open(dump_file_name, "wb") as f:
            pickle.dump(training_data, f)
            pickle.dump(testing_data, f)
        print(f"loaded data from csv file and pickled, {round(time.time() - timer_base)} seconds elapsed")

    X_train = [item[:-5] for item in training_data]
    Y_train = [item[-1] for item in training_data]
    X_test = [item[:-5] for item in testing_data]
    Y_test = [item[-1] for item in testing_data]
    print(f"grid search starting at {round(time.time() - timer_base)} seconds elapsed")

    # # grid search
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        for num_rounds in (300, 350, 400, 500, 600):
            for eta in (0.01, 0.025, 0.05):
                for subsample in (0.8, 0.85, 0.9, 0.95, 1):
                    for max_depth in (12, 15, 17, 20, 24):
                        results.append(executor.submit(run_parameter_set, X_train, Y_train, X_test, Y_test, num_rounds, eta, subsample, subsample, max_depth))

    print(f"finished grid search, {round(time.time() - timer_base)} seconds elapsed")
    with open("results.csv", 'w') as f:
        f.write("num_rounds,eta,subsample,max_depth,mean_training_error,median_training_error,min_testing_error,max_testing_error,mean_testing_error,median_testing_error,testing_error_stdev\n")
        for entry in results:
            f.write(entry.result())