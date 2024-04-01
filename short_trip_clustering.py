import pandas as pd
from sklearn.cluster import DBSCAN

# vars
CSV_FILE_PATH = '22data/jan22data/jan22_sorted_vacant_trips.csv'
TIME_CATEGORY = '0-3'
EPSILON = 0.1  # radius parameter for dbscan
MIN_SAMPLES = 10  # min number samples for dbscan

def read_data(file_path):
    return pd.read_csv(file_path)

def filter_data_by_time_category(data, time_category):
    return data[data['time_category'] == time_category]

def cluster_data(data):

    coordinates = data[['pickup.lat', 'pickup.lon']].values
    db = DBSCAN(eps=EPSILON, min_samples=MIN_SAMPLES).fit(coordinates)
    data['cluster'] = db.labels_
    return data

def get_cluster_centers(data):
    clusters = data.groupby('cluster')[['pickup.lat', 'pickup.lon']].mean()
    return clusters[clusters.index != -1]  # no noise clusters

def main():
    data = read_data(CSV_FILE_PATH)
    data_filtered = filter_data_by_time_category(data, TIME_CATEGORY)
    data_clustered = cluster_data(data_filtered)
    cluster_centers = get_cluster_centers(data_clustered)
    
    print("Cluster centers for '0-3' minute vacant trips:")
    print(cluster_centers)

if __name__ == "__main__":
    main()
