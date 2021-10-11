import os
import yaml
import csv
import json
from sklearn.metrics import accuracy_score


def read_yaml(path_to_yaml: str) -> dict:
    """this function access the parameters from config.yaml and params.yaml filesystem

    Args:
        path_to_yaml (str): path to .yaml filesystem

    Returns:
        dict: it reads the .yaml file content and return in a form of dictionary
    """
    with open (path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    return content

def create_directory(dirs: list):
    """this function iterate over the list of directories and create these director

    Args:
        dirs (list): list of directory paths
    """
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"directroy created at {dir_path}")

def save_data(data, data_path, index_status=False):
    """this function reads the dataframe and save it in the csv format

    Args:
        data (pd.DataFrames): test or train dataframe after spliting the dataset.
        data_path (str): path to save the datafram in csv format
        index_status (bool, optional): index parameter. Defaults to False.
    """
    data.to_csv(data_path, index=index_status)
    print(f"data saved at {data_path}")

def evaluate_accuracy(actual_values, predicted_values):
    """this function is used to calculate the accuracy of the model based

    Args:
        actual_values (pd.DataFrame): actual test values
        predicted_values (pd.DataFrame): predicted test values

    Returns:
        str: it returns the accuracy percentage in the from of string
    """
    accuracy = accuracy_score(actual_values, predicted_values)
    return accuracy

def save_reports(report: dict, report_path: str, indentation=4):
    """this function saves the accuracy in a form of dictionay in the json file  

    Args:
        report (dict): accuracy or other parameters like rms, r2, mae etc.
        report_path (str): path to save the report in a json file
        indentation (int, optional): indentation parameter. Defaults to 4.
    """              
    with open(report_path, "w") as f:
        json.dump(report, f, indent=indentation)
    print(f"reports are saved at {report_path}")  

