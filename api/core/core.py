# import csv
# from scheduler.scheduler import Scheduler
# from jobs.current_weather import get_current_weather_data

# class Core:
#     def __init__(self) -> None:
#         self.scheduler = Scheduler()
    
#     def should_run_scheduler(self) -> bool:
#         # If db has something AND can RUN (meaning the difference between last time stored 
#         #in the db and now is bigger than job_interval) OR has no record, return (True, none). If the db   
#         # has a time which was like 5 mins ago, and the job interval is like 10, return 5 which is the time until the next
#         # run should occur.. 
#         return True
    
#     def time_until_next_run(self) -> None:
#         pass
    

#     def load_locations(self) -> None:
#         with open('settings/location_list.csv', 'r') as csv_file:
#             reader = csv.reader(csv_file)
#             # Skip headers
#             next(reader)
#             for row in reader:
#                 print(row)
#                 kwargs = {'lat': row[0], 'lon': row[1]}
#                 self.scheduler.enqueue_job(get_current_weather_data, kwargs)

#     def start_scheduler(self) -> None:
#         self.scheduler.start_threaded()
        
#     def start_scheduler_threaded(self) -> None:
#         self.scheduler.start_threaded()
    
    
    
    
    