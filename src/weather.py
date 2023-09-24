import requests
from typing import Optional, Tuple, Union
from urllib.parse import urlencode, urlunparse
import os
import pandas as pd
from datetime import datetime
from requests.exceptions import RequestException
from abc import ABC, abstractmethod
from dotenv import load_dotenv
load_dotenv()



def factory_weather_client(config):
    if os.environ.get("WEATHER_CLIENT") == "MOCK":
        return MockWeatherClient(config)
    else:
        return WeatherClient(config)


class BaseWeatherClient(ABC):

    @abstractmethod
    def get_weather_data(self):
        """Fetch weather data."""
        pass


class MockWeatherClient(BaseWeatherClient):
    
    def __init__(self, config):
        self.config = config


    def get_weather_data(self):
        # Mock implementation for testing or local development
        file_path = os.path.join("data", "alabama", "birmingham", "1995", "316417a4-9ffc-4b84-a0a4-76c4f5cac8e8.csv")
        print(file_path)
        df = pd.read_csv(file_path)
        return df


class WeatherClient(BaseWeatherClient):
    """A client to interact with the Visual Crossing Weather API."""
    def __init__(self, config):
        self.config = config
        self.api_key: str = os.environ.get("VISUAL_CROSSING_API_KEY")
        if not self.api_key:
            raise EnvironmentError("VISUAL_CROSSING_API_KEY environment variable not set")
        

    def get_weather_data(self, chunk_size: Optional[int]=10, units: str="us", include: str="days", return_file_type: str="json") -> Union[pd.DataFrame, None]:
        """
        Get historical weather data for the specified location and date range. If data exists already on disk use it.

        Args:
        chunk_size Optional[int]=10: 
    
        Returns:
        Union[pd.DataFrame, None]: The requested weather data in a pandas DataFrame (or None in case of a failure).

        Raises:
        requests.exceptions.RequestException: If the request to the API is not a 200 code
        """

        date_list = self.__generate_date_list(chunk_size)
        date_ranges = self.__generate_date_ranges(date_list)
        

        dfs = []
        scheme = "https"
        netloc = "weather.visualcrossing.com"
        query_params: dict[str, str] = {
            "unitGroup": units,
            "include": include,
            "key": self.api_key,
            "contentType": return_file_type
            }

        for date_range in date_ranges:
            start_date, end_date = date_range

            
            path = f"/VisualCrossingWebServices/rest/services/timeline/{self.config['city']}%20{self.config['state']}/{start_date}/{end_date}"
            
            url_components = (scheme, netloc, path, None, urlencode(query_params), None)
            url = urlunparse(url_components)
            response = requests.get(url)

            if response.status_code != 200:
                raise RequestException(f"Request failed with status code {response.status_code}")
            else:
                json_data = response.json()
                df = pd.json_normalize(json_data['days'])
                dfs.append(df)

        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            # write_to_csv(self.config, df)
            return df
    

    def __generate_date_list(self, chunk_size: int) -> list[str]:
        """
        Generates a list of dates spaced by chunk size

        It is possible that the `end_date` might not be included in the generated date_list due to the fixed frequency interval.
        Therefore, we explicitly check if the `end_date` is in the `date_list`. If not, we append it to ensure that the range 
        accurately represents the entire span from the `start_date` to the `end_date`, inclusive of both endpoints."""
        
        start_date = f"{self.config['start_date']}"
        end_date = self.__add_year_to_date(start_date)
        date_list = pd.date_range(start=start_date, end=end_date, freq=f"{chunk_size}D").strftime('%Y-%m-%d').tolist()
        if end_date not in date_list:
            date_list.append(end_date)
        return date_list
        
        
    def __generate_date_ranges(self, date_list: list) -> list[Tuple[str, str]]:
        date_ranges = [(date_list[i], (pd.to_datetime(date_list[i + 1]) - pd.Timedelta(days=1)).strftime('%Y-%m-%d')) for i in range(0, len(date_list) - 2)]
        date_ranges += [(date_list[-2], date_list[-1])] 
        return date_ranges
    

    def __add_year_to_date(self, date: str) -> str:
        date = datetime.strptime(date, '%Y-%m-%d')
        date = date.replace(year=date.year + 1)
        date = date.strftime('%Y-%m-%d')
        return date