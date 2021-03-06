from src.utils.all_utils import read_yaml, create_directory, save_data
import os
import json
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import logging


def train_data(config_path, params_path):
    """this function is taking the training data from split_data_dir and train it on RandomForestClassifier. Model is saved at saved_model directory.

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

    # access training data
    train_data_filename = config["artifacts"]["train"]
    train_data_path = os.path.join(split_data_dir_path, train_data_filename)

    # access features and lables
    train_data = pd.read_csv(train_data_path)
    y_train = train_data["class"]
    x_train = train_data.drop("class", axis=1)
    # print(y_train.head(5))

    # access params
    n_jobs = params["model_params"]["RandomForest"]["params"]["n_jobs"]
    max_depth = params["model_params"]["RandomForest"]["params"]["max_depth"]
    n_estimators = params["model_params"]["RandomForest"]["params"]["n_estimators"]
    oob_score = params["model_params"]["RandomForest"]["params"]["oob_score"]
    random_state = params["base"]["random_state"]
    
    # buildign model
    logging.info(f"model training started")
    RFClassifier = RandomForestClassifier(random_state=random_state, n_jobs=n_jobs, max_depth=max_depth, n_estimators=n_estimators, oob_score=oob_score)
    RFClassifier.fit(x_train.values, y_train.values)
    logging.info(f"model training complete")

    # creating model directory and saving model
    model_dir = config["artifacts"]["model_dir"]
    model_dir_path = os.path.join(artifacts_dir, model_dir)
    create_directory([model_dir_path])
    logging.info(f"model directory created to save the model")

    model_filename = config["artifacts"]["model_filename"]
    model_file_path = os.path.join(model_dir_path, model_filename)

    joblib.dump(RFClassifier, model_file_path)
    logging.info(f"model saved at the model directory")

if __name__=="__main__":
    args = argparse.ArgumentParser()
    
    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")

    parsed_args = args.parse_args()

    try:
        logging.info(">>>>>>>>> Model Trainig Started >>>>>>>>>")
        train_data(config_path=parsed_args.config, params_path=parsed_args.params)
        logging.info("<<<<<<<<< Model Training Complete <<<<<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e