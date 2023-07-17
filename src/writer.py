import pandas as pd
import os
from utils import create_directory_if_not_exists

class Writer:
    def __init__(self, dir_path, filename):
        self.dir_path = create_directory_if_not_exists(dir_path)
        self.filename = filename

    def persist_to_parquet(self, df: pd.DataFrame) -> str:
        filepath = os.path.join(self.dir_path, f"{self.filename}.parquet")
        df.to_parquet(filepath)
        return filepath