import pandas as pd
import os
import uuid
import yaml


# def read_from_csv(config: dict) -> pd.DataFrame:
#     directory_path = os.path.join(config['weather_data_write_path'], config['state'], config['city'], config['start_date'].split('-')[])
#     file_name = os.listdir(directory_path)[0]
#     df = pd.read_csv(os.path.join(directory_path, file_name))
#     return df


# def write_to_csv(config: dict, df: pd.DataFrame) -> str:
#     directory_path = create_directory_if_not_exists(config['weather_data_write_path'], config['state'], config['city'], config['start_date'])
#     file_path = os.path.join(directory_path, f"{uuid.uuid4()}.csv")
#     df.to_csv(file_path)
#     return file_path
    

def load_config(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)


def create_directory_if_not_exists(*args):
    path = os.path.join(*args)
    if not os.path.exists(path):
        os.makedirs(path)
    return path