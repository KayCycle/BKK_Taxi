import pandas as pd
import matplotlib.pyplot as plt

def analyze_and_plot_mean_vacant_trip_time(file_path):
    
    df = pd.read_csv(file_path)
    
    # convert 'pickup.time' to datetime and extract the hour
    df['pickup_datetime'] = pd.to_datetime(df['pickup.date'] + ' ' + df['pickup.time'])
    df['hour'] = df['pickup_datetime'].dt.hour

    # convert 'trip.time' to numeric (mins or appropriate unit)
    df['trip.time'] = pd.to_numeric(df['trip.time'], errors='coerce')

    # group by hour and calculate the mean vacant trip time
    mean_vacant_trip_time_per_hour = df.groupby('hour')['trip.time'].mean()

    # plot result...
    plt.figure(figsize=(12, 6))
    bars = mean_vacant_trip_time_per_hour.plot(kind='bar', color='skyblue', xlabel='Hour of Day', ylabel='Mean Vacant Trip Time (minutes)', title='Mean Vacant Trip Time by Hour of Day')
    
    # text for bars
    for bar in bars.patches:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), round(bar.get_height(), 2), ha='center', va='bottom')

    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    
    # save plot
    plt.savefig('jan22_mean_vacant_trip_time_by_hour.png')

# example use
file_path = "22data/jan22data/jan22_sorted_vacant_trips.csv"
analyze_and_plot_mean_vacant_trip_time(file_path)
