import requests
from urllib.parse import urlencode, urlunparse
import os
import pandas as pd
from requests.exceptions import RequestException
from typing import Dict


class WeatherClient:
    """
    A client to interact with the Visual Crossing Weather API.

    Attributes:
    api_key (str): The API key for the Visual Crossing Weather API, retrieved from the environment variables.
    """
    def __init__(self):
        self.api_key: str = os.environ["VISUAL_CROSSING_API_KEY"]


    def get_historical_weather_data(self, city: str, state: str, start_date: str, end_date: str, units: str="us", include: str="days", file_type: str="json") -> pd.DataFrame:
        """
        Get historical weather data for the specified location and date range.

        Args:
        city (str): The city for which to retrieve weather data i.e. Houston
        state (str): The state for which to retrieve weather data i.e. Texas
        start_date (str): The start date for the weather data in the format 'yyyy-mm-dd'.
        end_date (str): The end date for the weather data in the format 'yyyy-mm-dd'.
        units (str, optional): The unit system to use for the weather data. Defaults to 'us'. Other options include "metric"
        include (str, optional): The level of detail to include in the data. Defaults to 'days'.
        file_type (str, optional): The file type of the response content. Defaults to 'json'. Other options "csv"

        Returns:
        dict: The requested weather data in JSON format.

        Raises:
        requests.exceptions.RequestException: If the request to the API is not a 200 code
        """
        scheme = "https"
        netloc = "weather.visualcrossing.com"
        path = f"/VisualCrossingWebServices/rest/services/timeline/{city}%20{state}/{start_date}/{end_date}"
        query_params: Dict[str, str] = {
        "unitGroup": units,
        "include": include,
        "key": self.api_key,
        "contentType": file_type

        }

        url_components = (scheme, netloc, path, None, urlencode(query_params), None)
        url = urlunparse(url_components)
        response = requests.get(url)

        if response.status_code != 200:
            raise RequestException(f"Request failed with status code {response.status_code}")
        else:
            json_data = response.json()
            df = pd.json_normalize(json_data['days'])

        return df