import os
import time
import pickle
import xgboost

import data_loader


if __name__ == "__main__":
    dump_file_name = "scenario_hack"
    model_file_name = "scenario_model"
    timer_base = time.time()

    if os.path.isfile(model_file_name):
        with open(model_file_name, "rb") as f:
            xgboost_model = pickle.load(f)
        print("loaded dumped model")
    else:
        if os.path.isfile(dump_file_name):
            with open(dump_file_name, "rb") as f:
                training_data = pickle.load(f)
                trend = pickle.load(f)
            print(f"loaded dumped data, {round(time.time() - timer_base)} seconds elapsed")
        else:
            training_data, trend = data_loader.load_training_data(verbose=True)
            with open(dump_file_name, "wb") as f:
                pickle.dump(training_data, f)
                pickle.dump(trend, f)
            print(f"loaded data from csv file and pickled, {round(time.time() - timer_base)} seconds elapsed")

        X_train = [item[:-5] for item in training_data]
        Y_train = [item[-1] - trend[item[4]] for item in training_data]

        parameters = {"eta": 0.025,
                    "seed": 0,
                    "subsample": 0.95,
                    "colsample_bytree": 0.95,
                    "objective": "reg:linear",
                    "max_depth": 20,
                    "min_child_weight": 1,
                    "verbosity": 0}
        matrix = xgboost.DMatrix(X_train, Y_train)
        xgboost_model = xgboost.train(parameters, matrix, num_boost_round=350)
        with open(model_file_name, "wb") as f:
            pickle.dump(xgboost_model, f)
        print(f"xgboost model trained and dumped in {round(time.time() - timer_base)} seconds")

    # prediction
    for filename in ("Scen1", "Scen2", "Scen2b", "Scen3", "Scen3b"):
        prediction_data = data_loader.load_testing_data(filename)

        predictions = xgboost_model.predict(xgboost.DMatrix(prediction_data)) + 1713364.6056634784
        with open(f"{filename}_results.csv", 'w') as f:
            for entry in predictions:
                f.write(str(entry) + '\n')
    
    print(f"prediction finished, {round(time.time() - timer_base)} seconds elapsed")