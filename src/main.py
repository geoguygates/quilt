from utils import load_config
from weather import WeatherClient
from quilt import draw_quilt



def main():
    try:
        config = load_config("src/config.yml")
    except FileNotFoundError as e:
        print(f"Error loading configuration: {e}")

    df = WeatherClient(config).get_weather_data()

    draw_quilt(config, df)

if __name__ == "__main__":
    main()