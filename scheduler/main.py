import os
import csv
from scheduler import JobScheduler
from jobs.current_weather import fetch_external_api
from data_manager import data_manager


def run():
    sched = JobScheduler(cycle_callback=data_manager.send_batch_data)
    path_to_locations_list = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)),
        'common',
        'settings',
        'location_list.csv')
    print(path_to_locations_list)
    with open(path_to_locations_list, 'r') as csv_file:
        reader = csv.reader(csv_file)
        # Skip headers
        next(reader)
        for row in reader:
            print(row)
            kwargs = {'lat': row[0], 'lon': row[1]}
            sched.enqueue_job(fetch_external_api, kwargs)
    sched.run()


if __name__ == '__main__':
    run()
