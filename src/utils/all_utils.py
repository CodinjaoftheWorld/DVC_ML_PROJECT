import os
import yaml
import csv
import json
from sklearn.metrics import accuracy_score


def read_yaml(path_to_yaml: str) -> dict:
    with open (path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    return content

def create_directory(dirs: list):
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"directroy created at {dir_path}")

def save_data(data, data_path, index_status=False):
    data.to_csv(data_path, index=index_status)
    print(f"data saved at {data_path}")

def evaluate_accuracy(actual_values, predicted_values):
    accuracy = accuracy_score(actual_values, predicted_values)
    return accuracy

def save_reports(report: dict, report_path: str, indentation=4):                   
    with open(report_path, "w") as f:
        json.dump(report, f, indent=indentation)
    print(f"reports are saved at {report_path}")  

