from src.utils.all_utils import read_yaml, create_directory, save_data
import os
import json
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split


def split_data(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    # read data and create dataframe
    remote_data_path = config["data_source"]
    df = pd.read_csv(remote_data_path)

    # create local directory to save artifacts
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

if __name__=="__main__":
    args = argparse.ArgumentParser()
    
    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")

    parsed_args = args.parse_args()

    split_data(config_path=parsed_args.config, params_path=parsed_args.params)



