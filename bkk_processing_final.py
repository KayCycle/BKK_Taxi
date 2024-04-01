import csv
import datetime
from geopy.distance import great_circle
from itertools import groupby
from operator import itemgetter
import glob
import re
from statistics import mean, median
from collections import Counter

def get_date_from_filename(filename):
    # assumes the filename contains a date in 'YYYYMMDD' format...
    match = re.search(r'\d{8}', filename)
    return match.group(0) if match else None

def calculate_distance(point1, point2):
    return great_circle(point1, point2).kilometers

def read_from_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        return list(reader)

def process_input(lines):
    sorted_data = []
    min_latitude = 13.49310
    max_latitude = 13.94913
    min_longitude = 100.32750
    max_longitude = 100.93963

    for split_line in lines:
        if (split_line[1] == '1' and split_line[8] == '1' and
            min_latitude <= float(split_line[2]) <= max_latitude and
            min_longitude <= float(split_line[3]) <= max_longitude):
            date = datetime.datetime.strptime(split_line[4], '%Y-%m-%d %H:%M:%S')
            sorted_data.append((split_line[0], date) + tuple(split_line))
            
    sorted_data.sort(key=itemgetter(0, 1))
    trips = []

    for taxi_id, items in groupby(sorted_data, key=itemgetter(0)):
        for_hire_status = None
        trip_points = []
        for _, _, *entry in items:
            if for_hire_status is not None and entry[7] != for_hire_status and len(trip_points) >= 2:
                trip_type = '0' if for_hire_status == '0' else '1'
                trips.append((taxi_id, trip_type, trip_points))
                trip_points = []
            for_hire_status = entry[7]
            trip_points.append(entry)
        if len(trip_points) >= 2:
            trip_type = '0' if for_hire_status == '0' else '1'
            trips.append((taxi_id, trip_type, trip_points))
    return trips

def write_trips_to_csv(trips, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['taxi.id', 'pickup.lat', 'pickup.lon', 'pickup.date', 'pickup.time',
                      'dropoff.lat', 'dropoff.lon', 'dropoff.date', 'dropoff.time', 'trip.time',
                      'trip.dist', 'trip.type', 'num.points']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for taxi_id, trip_type, trip_data in trips:
            pickup = trip_data[0]
            dropoff = trip_data[-1]
            pickup_datetime = datetime.datetime.strptime(pickup[4], '%Y-%m-%d %H:%M:%S')
            dropoff_datetime = datetime.datetime.strptime(dropoff[4], '%Y-%m-%d %H:%M:%S')
            trip_time = (dropoff_datetime - pickup_datetime).total_seconds() / 60.0
            trip_dist = sum(calculate_distance((float(trip_data[i][2]), float(trip_data[i][3])),
                                               (float(trip_data[i+1][2]), float(trip_data[i+1][3]))) for i in range(len(trip_data)-1))

            writer.writerow({
                'taxi.id': taxi_id,
                'pickup.lat': pickup[2],
                'pickup.lon': pickup[3],
                'pickup.date': pickup_datetime.date().isoformat(),
                'pickup.time': pickup_datetime.time().isoformat(timespec='seconds'),
                'dropoff.lat': dropoff[2],
                'dropoff.lon': dropoff[3],
                'dropoff.date': dropoff_datetime.date().isoformat(),
                'dropoff.time': dropoff_datetime.time().isoformat(timespec='seconds'),
                'trip.time': round(trip_time, 2),
                'trip.dist': round(trip_dist, 2),
                'trip.type': trip_type,
                'num.points': len(trip_data)
            })

def run_through_files(month_folder):
    # gett all .csv files in the folder and sort them by the date in the filename to put in chronological order
    csv_files = glob.glob(f'{month_folder}/*.csv.out')
    csv_files.sort(key=get_date_from_filename)
    
    all_trips = []

    for file_path in csv_files:
        lines = read_from_csv(file_path)
        trips = process_input(lines)
        all_trips.extend(trips)

    output_file = f'{month_folder}/aughalf2.csv'
    write_trips_to_csv(all_trips, output_file)

# run_through_files('22data/aug22data')

# file_path = '22data/jan22data/20220112.csv.out'
# input_text = read_from_csv(file_path)
# trips = process_input(input_text.strip())

# output_file = '22data/jan22output/202201_output.csv'
# write_trips_to_csv(trips, output_file)

#GUIDE
#arr = [VehicleID, gpsvalid, latitude, longitude, timestamp, speed, heading, for_hire_light, engine_acc]
    
#CALCULATE STATS

def calculate_basic_statistics(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        trips = list(reader)
    
    unique_taxis = {trip['taxi.id'] for trip in trips}
    busy_trips = [trip for trip in trips if trip['trip.type'] == '0']
    vacant_trips = [trip for trip in trips if trip['trip.type'] == '1']

    unclassified_trips = len(trips) - (len(busy_trips) + len(vacant_trips))
    print(f"Unclassified trips: {unclassified_trips}")
    
    busy_trip_dists = [float(trip['trip.dist']) for trip in busy_trips]
    vacant_trip_dists = [float(trip['trip.dist']) for trip in vacant_trips]
    
    busy_trip_times = [float(trip['trip.time']) for trip in busy_trips]
    vacant_trip_times = [float(trip['trip.time']) for trip in vacant_trips]
    
    pickup_dates = [trip['pickup.date'] for trip in trips]
    day_counts = Counter(pickup_dates)
    busiest_day, busiest_day_count = day_counts.most_common(1)[0]

    # Calculate the mean number of trips per day per taxi correctly
    days_in_month = 31 # Unique days
    mean_trips_per_day_per_taxi = len(trips) / (days_in_month * len(unique_taxis))
    
    statistics = {
        'total_number_of_unique_taxis': len(unique_taxis),
        'total_number_of_trips': len(trips),
        'number_of_busy_trips': len(busy_trips),
        'number_of_vacant_trips': len(vacant_trips),
        'mean_distance_of_busy_trips': mean(busy_trip_dists),
        'mean_distance_of_vacant_trips': mean(vacant_trip_dists),
        'median_distance_of_busy_trips': median(busy_trip_dists),
        'median_distance_of_vacant_trips': median(vacant_trip_dists),
        'mean_duration_of_busy_trips': mean(busy_trip_times),
        'mean_duration_of_vacant_trips': mean(vacant_trip_times),
        'median_duration_of_busy_trips': median(busy_trip_times),
        'median_duration_of_vacant_trips': median(vacant_trip_times),
        'mean_number_of_trips_per_day_per_taxi': mean_trips_per_day_per_taxi,
        'busiest_day': busiest_day,
        'busiest_day_count': busiest_day_count,
    }
    
    return statistics


# Example usage
file_path = '22data/aug22data/aug22.csv'  # path to csv
statistics = calculate_basic_statistics(file_path)
for stat, value in statistics.items():
    print(f"{stat}: {value}")




