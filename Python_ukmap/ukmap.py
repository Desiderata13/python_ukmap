import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# Define the bounding box for the UK map
UK_BOUNDS = (50.681, 57.985, -10.592, 1.6848)

def load_data():
    # Load and preprocess sensor data
    df = pd.read_csv('GrowLocations.csv')
    df = df[['Serial', 'Latitude', 'Longitude']].drop_duplicates('Serial').reset_index(drop=True)
    df.columns = ['SensorID', 'Longitude', 'Latitude']
    df['SensorID'] = df['SensorID'].astype(str).str.split('.').str[0]
    df = df[(df['Longitude'] >= UK_BOUNDS[2]) & (df['Longitude'] <= UK_BOUNDS[3]) &
            (df['Latitude'] >= UK_BOUNDS[0]) & (df['Latitude'] <= UK_BOUNDS[1])]
    return df

def scale_coordinates(coords, img_size):
    # Convert geographical coordinates to pixel coordinates
    lon_bounds, lat_bounds = (UK_BOUNDS[2], UK_BOUNDS[3]), (UK_BOUNDS[0], UK_BOUNDS[1])
    x = np.interp(coords[1], lon_bounds, (0, img_size[0]))
    y = np.interp(coords[0], lat_bounds, (img_size[1], 0))  # Invert y for correct orientation
    return int(x), int(y)

def plot_map():
    # Load data and create a map with sensor locations
    sensor_data = load_data()
    sensor_coords = list(zip(sensor_data['Latitude'], sensor_data['Longitude']))

    # Open the map image and prepare for drawing
    base_map = Image.open('map7.png', 'r')
    draw = ImageDraw.Draw(base_map)

    lon_bounds, lat_bounds = (UK_BOUNDS[2], UK_BOUNDS[3]), (UK_BOUNDS[0], UK_BOUNDS[1])

    # Convert geographical coordinates to pixel coordinates for all sensors
    pixel_coords = [scale_coordinates(coord, base_map.size) for coord in sensor_coords]

    # Draw ellipses at the pixel coordinates of sensor locations on the map
    for pixel_coord in pixel_coords:
        draw.ellipse([pixel_coord[0], pixel_coord[1], pixel_coord[0] + 10, pixel_coord[1] + 10], fill=(66, 163, 5))

    # Set up the plot with custom ticks and labels
    x_ticks = np.linspace(UK_BOUNDS[2], UK_BOUNDS[3], num=7)
    y_ticks = np.linspace(UK_BOUNDS[0], UK_BOUNDS[1], num=8)[::-1]

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(base_map)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_xticks(np.interp(np.linspace(UK_BOUNDS[2], UK_BOUNDS[3], num=7), lon_bounds, (0, base_map.size[0])))
    ax.set_yticks(np.interp(y_ticks, lat_bounds, (base_map.size[1], 0)))
    ax.set_xticklabels([round(x, 4) for x in x_ticks])
    ax.set_yticklabels([round(y, 4) for y in y_ticks])
    plt.show()

# Execute the plot_map function
plot_map()
