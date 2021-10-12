from src.utils.all_utils import read_yaml, create_directory, logging
import os
import json
import argparse
import pandas as pd
import logging


def get_data(config_path):
    """this function is used to get the read the data from path mentioned in config.yaml file, save the data at artifacts/raw_local_dir

    Args:
        config_path (str): paths for reading the data and saving the data in config.yaml files
    """
    config = read_yaml(config_path)

    # read data and create dataframe
    remote_data_path = config["data_source"]
    df = pd.read_csv(remote_data_path)

    # create local directory to save artifacts
    artifacts_dir = config["artifacts"]["artifacts_dir"]
    raw_local_dir = config["artifacts"]["raw_local_dir"]
    raw_local_file = config["artifacts"]["raw_local_file"]

    raw_local_dir_path = os.path.join(artifacts_dir, raw_local_dir)
    create_directory([raw_local_dir_path])
    logging.info(f"raw local directory created")
    
    raw_local_dir_file = os.path.join(raw_local_dir_path, raw_local_file)
    df.to_csv(raw_local_dir_file, sep=",", index=False)
    logging.info(f"data save at raw local directory")
    # print(f"data save at raw local directory")



if __name__=="__main__":
    args = argparse.ArgumentParser()
    
    args.add_argument("--config", "-c", default="config/config.yaml")

    parsed_args = args.parse_args()

    try:
        logging.info(">>>>>>>>> Data Loading Started >>>>>>>>>")
        get_data(config_path=parsed_args.config)
        logging.info("<<<<<<<<< Data Loading Complete <<<<<<<<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e



