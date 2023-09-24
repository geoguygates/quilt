from utils import load_config
from weather import factory_weather_client
from quilt import draw_quilt



def generate_plot():
    try:
        config = load_config("src/config.yml")
    except FileNotFoundError as e:
        print(f"Error loading configuration: {e}")

    weather_client = factory_weather_client(config)
    df =  weather_client.get_weather_data()

    draw_quilt(config, df)

if __name__ == "__main__":
    generate_plot()