import logging
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.executors.asyncio import AsyncIOExecutor
from queue import Queue
from typing import Callable
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

logging.basicConfig(filename='job_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Scheduler:
    def __init__(self, interval: int = 15, cycle_trigger: Callable[[], None] = lambda: None) -> None:
        # self.scheduler = BlockingScheduler(executors={'default': AsyncIOExecutor()}, 
        #                                   job_defaults={'misfire_grace_time': 10, 'max_instances': 5})
        self.curr_num_jobs = 0
        self.total_num_jobs = 0
        self.cycle_trigger = cycle_trigger
        self.scheduler = BlockingScheduler(job_defaults={'misfire_grace_time': 10, 'max_instances': 5})
        self.interval = interval
        self.job_queue = Queue()
        self.scheduler.add_listener(self.listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def run(self) -> None:
        """Run the scheduler"""
        logger.info("Starting the scheduler.")
        self.total_num_jobs = self.job_queue.qsize()
        self.schedule_jobs()
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()
            logger.info("Scheduler has been shut down.")

    def enqueue_job(self, fn, kwargs) -> None:
        """Add a job to the scheduler's queue"""
        self.job_queue.put((fn, kwargs))


    def schedule_jobs(self) -> None:
        """Schedule all jobs in the queue"""
        while not self.job_queue.empty():
            fn, kwargs = self.job_queue.get()
            self.scheduler.add_job(fn, 'interval', seconds=self.interval, kwargs=kwargs)

    def listener(self, event) -> None:
        """Listener for job events"""
        self.curr_num_jobs += 1
        if self.is_cycle():
            self.cycle_trigger()
            self.curr_num_jobs = 0
            
        if event.exception:
            logger.error(f"Job {event.job_id} raised an exception: {event.exception}")
        else:
            logger.info(f"Job {event.job_id} executed successfully.")
    
    def is_cycle(self):
        return self.curr_num_jobs == self.total_num_jobs

