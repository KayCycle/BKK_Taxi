#GUIDE
#arr = [VehicleID, gpsvalid, latitude, longitude, timestamp, speed, heading, for_hire_light, engine_acc]

import csv
import datetime
import geopy
from itertools import groupby
from operator import itemgetter
from pathlib import Path
from geopy.distance import great_circle

def calculate_distance(point1, point2):
    return great_circle(point1, point2).kilometers

def read_from_csv(file_path):
    path = Path(file_path)
    with path.open('r') as csvfile:
        reader = csv.reader(csvfile)
        lines = [','.join(row) for row in reader]
    return '\n'.join(lines)

def process_input(input_text):
    lines = input_text.splitlines()
    sorted_data = []

    print("started")

    # define lat and lon boundaries
    min_latitude = 13.49310
    max_latitude = 13.94913
    min_longitude = 100.32750
    max_longitude = 100.93963

    for line in lines:
        split_line = line.split(',')
        
        # check if gpsvalid (arr[1]) is '1' and engine_acc (arr[8]) is '1' and point is within the boundaries
        if (split_line[1] == '1' and split_line[8] == '1' and 
            min_latitude <= float(split_line[2]) <= max_latitude and 
            min_longitude <= float(split_line[3]) <= max_longitude):
            
            # date and store it along with the data
            date = datetime.datetime.strptime(split_line[4], '%Y-%m-%d %H:%M:%S')
            sorted_data.append((split_line[0], date) + tuple(split_line))

    # sort data by taxi ID then by date
    sorted_data.sort(key=itemgetter(0, 1))

    # group the data by taxi ID and extract trips
    trips = {}
    for taxi_id, items in groupby(sorted_data, key=itemgetter(0)):
        trips[taxi_id] = {'busy': [], 'vacant': []}
        for_hire_status = None
        trip_points = []

        for _, _, *entry in items:
            current_for_hire_status = entry[7]
            if for_hire_status is not None and current_for_hire_status != for_hire_status:
                if len(trip_points) >= 2:  # make sure each trip has at least 2 consecutive points
                    trip_type = 'busy' if for_hire_status == '0' else 'vacant'
                    trips[taxi_id][trip_type].append(trip_points)
                trip_points = []
            trip_points.append(entry)
            for_hire_status = current_for_hire_status
            current_for_hire_status = entry[7]

        # check if there is a trip at end of the data
        if len(trip_points) >= 2:  # check that the last trip has at least 2 consecutive points
            trip_type = 'busy' if for_hire_status == '0' else 'vacant'
            trips[taxi_id][trip_type].append(trip_points)

    return trips

def write_trips_to_csv(trips, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['taxi.id', 'pickup.lat', 'pickup.lon', 'pickup.date', 'pickup.time', 'dropoff.lat', 'dropoff.lon', 'dropoff.date', 'dropoff.time', 'trip.time', 'trip.dist', 'trip.type', 'num.points']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for taxi_id, taxi_trips in trips.items():
            for trip_type, trip_list in taxi_trips.items():
                for trip in trip_list:
                    if len(trip) >= 2:
                        pickup = trip[0]
                        dropoff = trip[-1]
                        pickup_datetime = datetime.datetime.strptime(pickup[4], '%Y-%m-%d %H:%M:%S')
                        dropoff_datetime = datetime.datetime.strptime(dropoff[4], '%Y-%m-%d %H:%M:%S')
                        trip_time = (dropoff_datetime - pickup_datetime).total_seconds() / 60.0
                        trip_dist = sum(calculate_distance((trip[i][2], trip[i][3]), (trip[i+1][2], trip[i+1][3])) for i in range(len(trip)-1))
                        
                        writer.writerow({
                            'taxi.id': taxi_id,
                            'pickup.lat': pickup[2],
                            'pickup.lon': pickup[3],
                            'pickup.date': pickup_datetime.date(),
                            'pickup.time': pickup_datetime.time(),
                            'dropoff.lat': dropoff[2],
                            'dropoff.lon': dropoff[3],
                            'dropoff.date': dropoff_datetime.date(),
                            'dropoff.time': dropoff_datetime.time(),
                            'trip.time': round(trip_time, 2),
                            'trip.dist': round(trip_dist, 2),
                            'trip.type': '0' if trip_type == 'busy' else '1',
                            'num.points': len(trip)
                        })

file_path = 'put file path here'
input_text = read_from_csv(file_path)
trips = process_input(input_text.strip())

output_file = 'put output file path here'
write_trips_to_csv(trips, output_file)

#GUIDE
#arr = [VehicleID, gpsvalid, latitude, longitude, timestamp, speed, heading, for_hire_light, engine_acc]



