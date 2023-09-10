from utils import load_config
from weather import WeatherClient
from quilt import render_quilt



def main():
    config = load_config("src/config.yml")
    weatherclient = WeatherClient()

    historical_weather_data_df = weatherclient.get_historical_weather_data(city="austin", state="texas", year="1997")
    
    render_quilt(historical_weather_data_df)


if __name__ == "__main__":
    main()