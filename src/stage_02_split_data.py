from src.utils.all_utils import read_yaml, create_directory, save_data
import os
import json
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
import logging

def split_data(config_path, params_path):
    """this function is used to read the data from raw_local_dir and split the data in the train and test set and save it again at split_data_dir directory by accessing the paths from confg.yaml and params.yaml files.

    Args:
        config_path (str): path to config.yaml file
        params_path (str): path to params.yaml file
    """
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    # read data and create dataframe
    remote_data_path = config["data_source"]
    df = pd.read_csv(remote_data_path)

    # # access local directory and saved artifacts
    artifacts_dir = config["artifacts"]["artifacts_dir"]
    raw_local_dir = config["artifacts"]["raw_local_dir"]
    raw_local_file = config["artifacts"]["raw_local_file"]

    raw_local_dir_path = os.path.join(artifacts_dir, raw_local_dir)
    raw_local_dir_file = os.path.join(raw_local_dir_path, raw_local_file)

    data = pd.read_csv(raw_local_dir_file)

    # creating split data directory
    split_data_dir = config["artifacts"]["split_data_dir"]
    split_data_dir_path = os.path.join(artifacts_dir, split_data_dir)
    create_directory([split_data_dir_path])
    logging.info(f"split data directory created to save test and train sets")

    # access params
    split_ratio = params["base"]["test_size"]
    random_state = params["base"]["random_state"]
    
    # split and save dataset
    train, test = train_test_split(data, test_size=split_ratio, random_state=random_state)

    train_data_filename = config["artifacts"]["train"]
    test_data_filename = config["artifacts"]["test"]

    train_data_path = os.path.join(split_data_dir_path, train_data_filename)
    test_data_path = os.path.join(split_data_dir_path, test_data_filename)

    for dt, dt_path in (train, train_data_path), (test, test_data_path):
        save_data(dt, dt_path)

    logging.info(f"test and train data saved at split_data_dir")

if __name__=="__main__":
    args = argparse.ArgumentParser()
    
    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")

    parsed_args = args.parse_args()

    try:
        logging.info(">>>>>>>>> Data Spliting Started >>>>>>>>>")
        split_data(config_path=parsed_args.config, params_path=parsed_args.params)
        logging.info("<<<<<<<<< Data Spliting Complete <<<<<<<<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e


