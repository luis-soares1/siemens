import csv
import asyncio
from scheduler import Scheduler
from jobs.current_weather import fetch_and_populate

def run():
    sched = Scheduler()

    with open('settings/location_list.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        # Skip headers
        next(reader)
        for row in reader:
            print(row)
            kwargs = {'lat': row[0], 'lon': row[1]}
            sched.enqueue_job(fetch_and_populate, kwargs)

    sched.run_forever()

if __name__ == '__main__':
    run()