import matplotlib.pyplot as plt
import pandas as pd
import os
from sklearn.cluster import DBSCAN
import numpy as np

def plot_vacant_trips_with_clustering(file_path, hours, day, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    df = pd.read_csv(file_path)
    
    df['pickup_datetime'] = pd.to_datetime(df['pickup.date'] + ' ' + df['pickup.time'])
    df['pickup_hour'] = df['pickup_datetime'].dt.hour
    df['pickup_day'] = df['pickup_datetime'].dt.day
    
    colors = {
        "0-3": "red",
        "3-6": "orange",
        "6-10": "green",
        "10-15": "blue",
        "15+": "purple"
    }

    for hour in hours:
        df_filtered = df[(df['pickup_hour'] == hour) & (df['pickup_day'] == day)]
        
        plt.figure(figsize=(10, 6))

        for category, color in colors.items():
            df_category = df_filtered[df_filtered['time_category'] == category]
            if not df_category.empty:
                # actual dbscan being performed
                coords = df_category[['pickup.lat', 'pickup.lon']].to_numpy()
                db = DBSCAN(eps=0.01, min_samples=5).fit(coords)
                labels = db.labels_

                # get unique labsls
                unique_labels = set(labels)
                for k in unique_labels:
                    if k == -1:
                        # Noise
                        col = 'k'
                    else:
                        col = color
                    class_member_mask = (labels == k)
                    xy = coords[class_member_mask]
                    plt.plot(xy[:, 1], xy[:, 0], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6, alpha=0.5, label=f'Cluster {k}' if k != -1 else 'Noise')

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(f'Vacant Trips for Hour {hour} on Day {day} with Clustering')
        plt.legend()

        save_path = os.path.join(save_dir, f'vacant_trips_hour_{hour}_day_{day}_clusters.png')
        plt.savefig(save_path)
        plt.close()

file_path = "22data/jan22data/jan22_sorted_vacant_trips.csv"
hours = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23]  # test hours to plot
days = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31] # test days to plot
save_dir = "22data/jan22data/jan22_plot_clusters"  # save directory

for day in days:
    plot_vacant_trips_with_clustering(file_path, hours, day, save_dir)
