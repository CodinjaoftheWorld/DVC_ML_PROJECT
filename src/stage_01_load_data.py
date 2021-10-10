from src.utils.all_utils import read_yaml, create_directory
import os
import json
import argparse
import pandas as pd


def get_data(config_path):
    config = read_yaml(config_path)

    # read data and create dataframe
    remote_data_path = config["data_source"]
    df = pd.read_csv(remote_data_path)

    # create local directory to save artifacts
    artifacts_dir = config["artifacts"]["artifacts_dir"]
    raw_local_dir = config["artifacts"]["raw_local_dir"]
    raw_local_file = config["artifacts"]["raw_local_file"]

    raw_local_dir_path = os.path.join(artifacts_dir, raw_local_dir)
    # print(raw_local_dir_path)
    create_directory([raw_local_dir_path])
    
    raw_local_dir_file = os.path.join(raw_local_dir_path, raw_local_file)
    df.to_csv(raw_local_dir_file, sep=",", index=False)
    print(f"data save at raw local directory")



if __name__=="__main__":
    args = argparse.ArgumentParser()
    
    args.add_argument("--config", "-c", default="config/config.yaml")

    parsed_args = args.parse_args()

    get_data(config_path=parsed_args.config)



