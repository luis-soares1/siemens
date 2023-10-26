import os
import logging
from settings.config import get_settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from queue import Queue
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR


logging.basicConfig(filename='job_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Scheduler():
    def __init__(self) -> None:
        executors = {
            'default': AsyncIOExecutor()
        }
        self.scheduler = AsyncIOScheduler(executors=executors, job_defaults={'misfire_grace_time': 10})
        self.interval = get_settings().job_interval
        self.job_queue = Queue()
    # If a job fails, add it back to the queue, at the front. Maybe use deque
    def start(self) -> None:
        print(f"Total jobs scheduled: {self.get_queue_length()}")
        try:
            while not self.job_queue.empty():
                fn, kwargs = self.job_queue.get()
                self.scheduler.add_job(fn, 'interval', seconds=self.interval, kwargs={**kwargs}, max_instances=5)
            self.scheduler.add_listener(self.listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()

    def enqueue_job(self, fn, kwargs) -> None:
        self.job_queue.put((fn, kwargs))
    
    def listener(self, event) -> None:
        if event.exception:
            logger.error(f"Job {event.job_id} raised an exception: {event.exception}")
        else:
            print(f"Job {event.job_id} executed successfully.")
        
    def get_queue_length(self) -> int:
        return self.job_queue.qsize()
