import pandas as pd

def load_top_performers(filepath):
    """Load the list of top performers from a CSV file."""
    return pd.read_csv(filepath)

def load_trip_data(filepath):
    """Load trip data from a CSV file."""
    return pd.read_csv(filepath)

def filter_trips_by_top_performers(trip_data, top_performers):
    """Filter the trips to only include those done by the top performers."""
    # Create a set of top performer taxi IDs for fast lookup
    top_performer_ids = set(top_performers['taxi.id'])
    # Filter the trips
    return trip_data[trip_data['taxi.id'].isin(top_performer_ids)]

def main():
    # Paths to your data
    top_performers_path = '22data/jan22data/jan22_taxi_performances/top_100_taxis.csv'
    trip_data_path = '22data/jan22data/jan22.csv'
    output_path = '22data/jan22data/jan22_top_performers_trips.csv'
    
    # Load data
    top_performers = load_top_performers(top_performers_path)
    trip_data = load_trip_data(trip_data_path)
    
    # Filter data
    filtered_trips = filter_trips_by_top_performers(trip_data, top_performers)
    
    # Save the filtered trips
    filtered_trips.to_csv(output_path, index=False)

if __name__ == "__main__":
    main()
