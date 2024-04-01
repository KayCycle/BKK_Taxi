import pandas as pd
import matplotlib.pyplot as plt

def get_taxi_statistics(file_path):
    df = pd.read_csv(file_path)
    # make sure trip.time is numeric and filter out anything else
    df['trip.time'] = pd.to_numeric(df['trip.time'], errors='coerce')
    # remove error rows
    df.dropna(subset=['trip.time'], inplace=True)
    
    # group by taxi.id and find mean trip time and trip count
    taxi_stats = df.groupby('taxi.id').agg(
        avg_vacant_trip_time=('trip.time', 'mean'),
        number_of_trips=('taxi.id', 'size')
    ).reset_index()
    
    # filter out taxis w less than 30 trips per month
    taxi_stats = taxi_stats[taxi_stats['number_of_trips'] >= 30]
    
    # get top 100 & bottom 100 taxis
    top_taxis = taxi_stats.nsmallest(100, 'avg_vacant_trip_time')
    bottom_taxis = taxi_stats.nlargest(100, 'avg_vacant_trip_time')
    
    # csv save
    top_taxis.to_csv('top_100_taxis.csv', index=False)
    bottom_taxis.to_csv('bottom_100_taxis.csv', index=False)
    
    return top_taxis, bottom_taxis

def plot_taxi_locations(df, taxi_ids, output_filename, title):
    plt.figure(figsize=(10, 6))
    for taxi_id in taxi_ids:
        taxi_data = df[df['taxi.id'] == taxi_id]
        plt.scatter(taxi_data['pickup.lon'], taxi_data['pickup.lat'], alpha=0.5)
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(title)
    plt.savefig(output_filename)
    plt.close()

# path to csv file (ignore)
file_path = "22data/jan22data/jan22_sorted_vacant_trips.csv"

# taxi stats
top_taxis, bottom_taxis = get_taxi_statistics(file_path)

# read file for plootting
df = pd.read_csv(file_path)

# plot and save
plot_taxi_locations(df, top_taxis['taxi.id'], 'top_100_taxis.png', 'Top 100 Taxis with Lowest Average Vacant Trip Time')
plot_taxi_locations(df, bottom_taxis['taxi.id'], 'bottom_100_taxis.png', 'Bottom 100 Taxis with Highest Average Vacant Trip Time')
