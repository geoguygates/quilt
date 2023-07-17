from weather import WeatherClient
from writer import Writer

def main():
    client = WeatherClient()
    df = client.get_historical_weather_data(city="austin", state='texas', start_date="1997-01-01", end_date="1997-01-01")
    writer = Writer(r"C:\Users\David Gate\Documents\repos\quilt\data_lake", "January 1997")
    writer.persist_to_parquet(df)


if __name__ == "__main__":
    main()