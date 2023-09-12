import pandas as pd
import os
import uuid
import yaml



class Writer:
    def __init__(self, config):
        self.config = config
        self.directory_path = create_directory_if_not_exists(config['weather_data_write_path'], self.config['state'], self.config['city'], self.config['year'])


    def write_to_csv(self, df: pd.DataFrame) -> str:
        file_path = os.path.join(self.directory_path, f"{uuid.uuid4()}.csv")
        df.to_csv(file_path)
        return file_path
    

class Reader:
    def __init__(self, config):
        self.config = config
    

    def read_from_csv(self) -> pd.DataFrame:
        directory_path = os.path.join(self.config['weather_data_write_path'], self.config['state'], self.config['city'], self.config['year'])
        file_name = os.listdir(directory_path)[0]
        df = pd.read_csv(os.path.join(directory_path, file_name))
        return df
    

def load_config(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)


def create_directory_if_not_exists(*args):
    path = os.path.join(*args)
    if not os.path.exists(path):
        os.makedirs(path)
    return path