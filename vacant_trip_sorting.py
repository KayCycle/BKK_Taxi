import csv

def categorize_trip_time(trip_time):
    if trip_time <= 3:
        return '0-3'
    elif trip_time <= 6:
        return '3-6'
    elif trip_time <= 10:
        return '6-10'
    elif trip_time <= 15:
        return '10-15'
    else:
        return '15+'

def read_and_categorize_vacant_trips(input_file_path, output_file_path):
    with open(input_file_path, mode='r', newline='') as csvfile, \
         open(output_file_path, mode='w', newline='') as output_csvfile:
        
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ['time_category']  # add new time_category field
        writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
        
        writer.writeheader()

        print("started")

        # process and write to rows that are vacant
        for row in reader:
            if row['trip.type'] == '1':
                trip_time = float(row['trip.time'])
                row['time_category'] = categorize_trip_time(trip_time)
                writer.writerow(row)

# path definitions
input_file_path = '22data/jan22data/jan22_work.csv'
output_file_path = '22data/jan22data/sorted_vacant_trips.csv'

read_and_categorize_vacant_trips(input_file_path, output_file_path)
