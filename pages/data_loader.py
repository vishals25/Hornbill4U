import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load dataset (using relative paths)
df = pd.read_excel('data/horn_bill_telemetry.xlsx')
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%m/%d/%y %H:%M')

# Extract month and year
df['month'] = df['timestamp'].dt.month
df['month_name'] = df['timestamp'].dt.strftime('%B')
df['year'] = df['timestamp'].dt.year

# Create geometry for the GeoDataFrame
geometry = [Point(xy) for xy in zip(df['location-long'], df['location-lat'])]
geo_df = gpd.GeoDataFrame(df, geometry=geometry)
geo_df.set_crs(epsg=4326, inplace=True)

map_options = {
    'OpenStreetMap': 'open-street-map',
    'CartoDB Positron': 'carto-positron',
    'CartoDB Dark Matter': 'carto-darkmatter'
}

# Load cluster dataset
cluster_df = pd.read_excel('data/data_with_clusters.xlsx')
cluster_df['timestamp'] = pd.to_datetime(cluster_df['timestamp'])

# Load bird speed dataset
bird_data = pd.read_excel('data/bird_speed_analysis.xlsx', engine='openpyxl')

# Load migration data
migration_data = pd.read_csv('data/migration.csv')
print(migration_data.columns)  # Check all column names