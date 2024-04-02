import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the path to the CSV file
CSV_FILE_PATH = '22data/jan22data/jan22_sorted_vacant_trips.csv'
# Define the time category of interest
TIME_CATEGORY = '0-3'
# save path
save_dir = "22data/jan22data"  # save directory

def read_data(file_path):
    return pd.read_csv(file_path)

def filter_data_by_time_category(data, time_category):
    return data[data['time_category'] == time_category]

def plot_heatmap(data):
    plt.figure(figsize=(10, 8))
    # Using hexbin for density plot
    plt.hexbin(data['pickup.lon'], data['pickup.lat'], gridsize=50, cmap='Reds', bins='log')
    plt.colorbar(label='Log10 of count')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Heatmap of 0-3 Minute Vacant Trips')

    save_path = os.path.join(save_dir, 'jan22_heatmap_vacant_trips.png')
    plt.savefig(save_path)
    plt.close()

def main():
    data = read_data(CSV_FILE_PATH)
    data_filtered = filter_data_by_time_category(data, TIME_CATEGORY)
    plot_heatmap(data_filtered)

if __name__ == "__main__":
    main()
