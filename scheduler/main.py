import csv
from scheduler import Scheduler
from jobs.current_weather import fetch_and_populate
from data_manager import data_manager

def run():
    sched = Scheduler(interval=5, cycle_trigger=data_manager.send_batch_data)
    
    with open('settings/location_list.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        # Skip headers
        next(reader)
        for row in reader:
            print(row)
            kwargs = {'lat': row[0], 'lon': row[1]}
            sched.enqueue_job(fetch_and_populate, kwargs)

    sched.run()

if __name__ == '__main__':
    run()