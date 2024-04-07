import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import numpy as np

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

def plot_taxi_locations_with_clustering(df, taxi_ids, output_filename, title):
    plt.figure(figsize=(10, 6))
    for taxi_id in taxi_ids:
        taxi_data = df[df['taxi.id'] == taxi_id]
        # Ensure there's enough data to cluster
        if len(taxi_data) < 3:
            continue
        # Prepare the data for clustering (convert to radians for Haversine distance)
        coords = taxi_data[['pickup.lat', 'pickup.lon']].values
        coords_radians = np.radians(coords)
        # Apply DBSCAN clustering
        db = DBSCAN(eps=0.1/6371., min_samples=10, algorithm='ball_tree', metric='haversine').fit(coords_radians)
        labels = db.labels_
        # Plot clusters
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        for cluster in range(n_clusters_):
            cluster_data = taxi_data[labels == cluster]
            plt.scatter(cluster_data['pickup.lon'], cluster_data['pickup.lat'], alpha=0.5, label=f'Taxi {taxi_id} Cluster {cluster}')
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(title)
    if n_clusters_ > 0:
        plt.legend(loc='upper right', fontsize='small', markerscale=2)
    plt.savefig(output_filename)
    plt.close()

def plot_all_taxi_locations_with_clustering_not_individual(df, taxi_ids, output_filename, title):
    plt.figure(figsize=(10, 6))
    # Filter the dataframe for all trips made by the specified taxi IDs
    all_taxi_data = df[df['taxi.id'].isin(taxi_ids)]
    # Ensure there's enough data to cluster
    if len(all_taxi_data) < 3:
        print("Not enough data for clustering.")
        return
    # Prepare the data for clustering (convert to radians for Haversine distance)
    coords = all_taxi_data[['pickup.lat', 'pickup.lon']].values
    coords_radians = np.radians(coords)
    # Apply DBSCAN clustering
    db = DBSCAN(eps=0.1/6371., min_samples=100, algorithm='ball_tree', metric='haversine').fit(coords_radians)
    labels = db.labels_
    # Plot clusters, excluding noise
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    for cluster in range(n_clusters_):
        cluster_data = all_taxi_data[labels == cluster]
        plt.scatter(cluster_data['pickup.lon'], cluster_data['pickup.lat'], alpha=0.5, label=f'Cluster {cluster}')
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(title)
    if n_clusters_ > 0:
        plt.legend(loc='upper right', fontsize='small', markerscale=2)
    plt.savefig(output_filename)
    plt.close()



# path to csv file (ignore)
file_path = "22data/jan22data/jan22_sorted_vacant_trips.csv"

# taxi stats
top_taxis, bottom_taxis = get_taxi_statistics(file_path)

# read file for plootting
df = pd.read_csv(file_path)

# plot and save
plot_all_taxi_locations_with_clustering_not_individual(df, top_taxis['taxi.id'], 'top_100_taxis_with_clustering.png', 'Top 100 Taxis with Lowest Average Vacant Trip Time')
# plot_all_taxi_locations_with_clustering_not_individual(df, bottom_taxis['taxi.id'], 'bottom_100_taxis_with_clustering.png', 'Bottom 100 Taxis with Highest Average Vacant Trip Time')
