import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_trip_data(filepath):
    """Load trip data from a CSV file."""
    return pd.read_csv(filepath)

def plot_density_contour(data, title, output_filename):
    """Plot a 2D density contour plot of the starting points."""
    plt.figure(figsize=(10, 8))
    sns.kdeplot(x=data['pickup.lon'], y=data['pickup.lat'], levels=20, color='blue', fill=True)
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.savefig(output_filename)
    plt.close()

def main():
    # File path to the trip data of top performers
    filepath = '22data/jan22data/jan22_top_performers/jan22_top_performers_trips.csv'
    
    # Load trip data
    trip_data = load_trip_data(filepath)
    
    # Filter data for busy and vacant trips
    busy_trips = trip_data[trip_data['trip.type'] == 0]  # Assuming 0 for busy, adjust as needed
    vacant_trips = trip_data[trip_data['trip.type'] == 1]  # Assuming 1 for vacant, adjust as needed

    # Plot density contour for busy trips
    plot_density_contour(busy_trips, 'Density Plot of Busy Trip Starting Points', 'busy_trips_density.png')

    # Plot density contour for vacant trips
    plot_density_contour(vacant_trips, 'Density Plot of Vacant Trip Starting Points', 'vacant_trips_density.png')

if __name__ == "__main__":
    main()
