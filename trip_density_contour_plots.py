import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_trip_data(filepath):
    
    return pd.read_csv(filepath)

def plot_density_contour(data, title, output_filename):
    #plot
    plt.figure(figsize=(10, 8))
    sns.kdeplot(x=data['pickup.lon'], y=data['pickup.lat'], levels=20, color='blue', fill=True)
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.savefig(output_filename)
    plt.close()

def main():
    # file path to top 100
    filepath = '22data/jan22data/jan22_top_performers/jan22_top_performers_trips.csv'
    
    # trops
    trip_data = load_trip_data(filepath)
    
    # filtering for busy and vacant
    busy_trips = trip_data[trip_data['trip.type'] == 0]  # Assuming 0 for busy, adjust as needed
    vacant_trips = trip_data[trip_data['trip.type'] == 1]  # Assuming 1 for vacant, adjust as needed

    #plot busy
    plot_density_contour(busy_trips, 'Density Plot of Busy Trip Starting Points', 'busy_trips_density.png')

    #plot vacant
    plot_density_contour(vacant_trips, 'Density Plot of Vacant Trip Starting Points', 'vacant_trips_density.png')

if __name__ == "__main__":
    main()
