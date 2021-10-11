from src.utils.all_utils import read_yaml, create_directory, save_data, evaluate_accuracy, save_reports
import os
import json
import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import accuracy_score



def evaluate(config_path, params_path):
    """this function takes the test data from slpit_data_dir, predict the labels and calculate the accuracy of the RFClassifier. Output of the model(accuracy) is saved at scores_dir in the form of json file.  

    Args:
        config_path (str): path to config.yaml file
        params_path (str): path to params.yaml file
    """
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    # access local directory and saved artifacts
    artifacts_dir = config["artifacts"]["artifacts_dir"]

    # access split data directory
    split_data_dir = config["artifacts"]["split_data_dir"]
    split_data_dir_path = os.path.join(artifacts_dir, split_data_dir)

    # access testing data
    test_data_filename = config["artifacts"]["test"]
    test_data_path = os.path.join(split_data_dir_path, test_data_filename)

    # access features and lables
    test_data = pd.read_csv(test_data_path)
    y_test = test_data["class"]
    x_test = test_data.drop("class", axis=1)

    # accessing model directory and saved model
    model_dir = config["artifacts"]["model_dir"]
    model_dir_path = os.path.join(artifacts_dir, model_dir)
    model_filename = config["artifacts"]["model_filename"]
    model_file_path = os.path.join(model_dir_path, model_filename)

    # creating scores directory and saving the report in json format
    scores_dir = config["artifacts"]["scores_dir"]
    scores_dir_path = os.path.join(artifacts_dir, scores_dir)
    create_directory([scores_dir_path])

    scores_filename = config["artifacts"]["scores_filename"]
    scores_file_path = os.path.join(scores_dir_path, scores_filename)

    RFClassifier = joblib.load(model_file_path)

    predicted_values = RFClassifier.predict(x_test.values)
    accuracy = evaluate_accuracy(y_test.values, predicted_values)
    # print(accuracy)

    scores = {
        "accuracy": accuracy,
    }

    save_reports(report=scores, report_path=scores_file_path)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    
    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")

    parsed_args = args.parse_args()

    evaluate(config_path=parsed_args.config, params_path=parsed_args.params)
