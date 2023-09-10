import requests
from typing import Optional, Tuple, Union
from urllib.parse import urlencode, urlunparse
import os
import pandas as pd
from requests.exceptions import RequestException
from typing import Dict


class WeatherClient:
    """A client to interact with the free Visual Crossing Weather API."""
    def __init__(self):
        self.api_key: str = os.environ["VISUAL_CROSSING_API_KEY"]


    def get_historical_weather_data(self, city: str, state: str, year: str, chunk_size: Optional[int] = 10, units: str="us", include: str="days", return_file_type: str="json") -> Union[pd.DataFrame, None]:
        """
        Get historical weather data for the specified location and date range. If data exists already on disk use it.

        Args:
        city (str): The city for which to retrieve weather data i.e. Houston
        state (str): The state for which to retrieve weather data i.e. Texas
        start_date (str): The start date for the weather data in the format 'yyyy-mm-dd'.
        end_date (str): The end date for the weather data in the format 'yyyy-mm-dd'.
        units (str, optional): The unit system to use for the weather data. Defaults to 'us'. Other options include "metric"
        include (str, optional): The level of detail to include in the data. Defaults to 'days'.
        return_file_type (str, optional): The file type of the response content. Defaults to 'json'. Other options "csv"

        Returns:
        Union[pd.DataFrame, None]: The requested weather data in a pandas DataFrame (or None in case of a failure).

        Raises:
        requests.exceptions.RequestException: If the request to the API is not a 200 code
        """
        
        date_list = self.__generate_date_list(year, chunk_size)
        date_ranges = self.__generate_date_ranges(date_list)
        
        dfs = []
        scheme = "https"
        netloc = "weather.visualcrossing.com"
        query_params: Dict[str, str] = {
            "unitGroup": units,
            "include": include,
            "key": self.api_key,
            "contentType": return_file_type
            }

        for date_range in date_ranges:
            start_date, end_date = date_range

            
            path = f"/VisualCrossingWebServices/rest/services/timeline/{city}%20{state}/{start_date}/{end_date}"
            
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
            return pd.concat(dfs, ignore_index=True)
        else:
            return None
    

    def __generate_date_list(self, year: str, chunk_size: int) -> list[str]:
        """It is possible that the `end_date` might not be included in the generated date_list due to the fixed frequency interval.
        Therefore, we explicitly check if the `end_date` is in the `date_list`. If not, we append it to ensure that the range 
        accurately represents the entire span from the `start_date` to the `end_date`, inclusive of both endpoints."""
        
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        date_list = pd.date_range(start=start_date, end=end_date, freq=f"{chunk_size}D").strftime('%Y-%m-%d').tolist()
        if end_date not in date_list:
            date_list.append(end_date)
        return date_list
        
        
    def __generate_date_ranges(self, date_list: list) -> list[Tuple[str, str]]:
        date_ranges = [(date_list[i], (pd.to_datetime(date_list[i + 1]) - pd.Timedelta(days=1)).strftime('%Y-%m-%d')) for i in range(0, len(date_list) - 2)]
        date_ranges += [(date_list[-2], date_list[-1])]  # Add the last date range separately
        return date_ranges