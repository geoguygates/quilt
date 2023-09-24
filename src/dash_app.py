import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from weather import factory_weather_client
from quilt import draw_quilt



dash_app = dash.Dash(__name__)

# Step 3: Define your Dash app and layout
dash_app.layout = html.Div([
    # Create input fields for the user to configure inputs (replace with your actual input fields)
    dcc.Input(id='input-city', type='text', placeholder='Enter city'),
    dcc.Input(id='input-state', type='text', placeholder='Enter state'),
    dcc.Input(id='input-start-date', type='text', placeholder='Enter start date'),
    dcc.Input(id='input-colors', type='number', placeholder='Enter number of colors'),
    
    # Button to trigger the plot generation
    html.Button('Generate Plot', id='generate-button'),
    
    # Area to display the plot
    html.Img(id='plot-output'),
])

# Step 4: Create a callback function
@dash_app.callback(Output('plot-output', 'src'),
    [Input('generate-button', 'n_clicks')],
    [
        dash.dependencies.State('input-city', 'value'),
        dash.dependencies.State('input-state', 'value'),
        dash.dependencies.State('input-start-date', 'value'),
        dash.dependencies.State('input-colors', 'value')
    ]
)
def generate_plot(n_clicks, city, state, start_date, num_colors):
    if not all([city, state, start_date, num_colors, n_clicks]):
        return dash.no_update

    config = {'city': city, 'state': state, 'start_date': start_date, 'num_colors': num_colors}
    print(f"Config: {config}")  # Check the configuration dictionary

    try:
        weather_client = factory_weather_client(config)
        df = weather_client.get_weather_data()
        print(f"DataFrame shape: {df.shape}")  # Check the shape of the DataFrame
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        src = draw_quilt(config, df)
        print(f"Source length: {len(src)}")  # Check the length of the source string

    except Exception as e:
        print(f"An error occurred: {e}")

    return src


# Run the Dash app
if __name__ == '__main__':
    dash_app.run_server(debug=True)