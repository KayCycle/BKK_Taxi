import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
import os

# Define the path to the CSV file
CSV_FILE_PATH = '22data/jan22data/jan22_sorted_vacant_trips.csv'
# Define the time category of interest
TIME_CATEGORY = '0-3'
# save path
save_dir = "22data/jan22data"  # save directory
EPSILON = 0.1  # Consider this as the radius of neighborhood in kilometers, adjust as necessary
MIN_SAMPLES = 25 # Minimum samples in a neighborhood for a point to be considered as a core point

def read_data(file_path):
    return pd.read_csv(file_path)

def filter_data_by_time_category(data, time_category):
    return data[data['time_category'] == time_category]

def apply_dbscan(data, eps, min_samples):
    # Convert to radians for sklearn Haversine metric
    coords = np.radians(data[['pickup.lat', 'pickup.lon']])
    db = DBSCAN(eps=eps/6371, min_samples=min_samples, algorithm='ball_tree', metric='haversine').fit(coords)
    data['cluster'] = db.labels_
    return data

def filter_clusters_with_minimum_trips(data, min_trips):
    # Count the number of trips in each cluster
    cluster_counts = data['cluster'].value_counts()
    # Filter clusters having trips >= MIN_TRIPS and exclude noise (cluster = -1)
    valid_clusters = cluster_counts[(cluster_counts >= min_trips) & (cluster_counts.index != -1)].index
    return data[data['cluster'].isin(valid_clusters)]

def plot_clusters(data):
    plt.figure(figsize=(12, 8))
    # Plot each cluster with a different color
    clusters = data['cluster'].unique()
    for cluster in clusters:
        cluster_data = data[data['cluster'] == cluster]
        plt.scatter(cluster_data['pickup.lon'], cluster_data['pickup.lat'], s=10, label=f'Cluster {cluster}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Clusters of 0-3 Minute Vacant Trips')
    plt.legend()
    
    save_path = os.path.join(save_dir, 'jan22_25clus_short_trips.png')
    plt.savefig(save_path)
    plt.close()


def main():
    data = read_data(CSV_FILE_PATH)
    data_filtered = filter_data_by_time_category(data, TIME_CATEGORY)
    data_clustered = apply_dbscan(data_filtered, EPSILON, MIN_SAMPLES)
    data_final = filter_clusters_with_minimum_trips(data_clustered, MIN_SAMPLES)
    plot_clusters(data_final)

if __name__ == "__main__":
    main()

