import logging
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.executors.asyncio import AsyncIOExecutor
from queue import Queue
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

logging.basicConfig(filename='job_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Scheduler:
    def __init__(self, interval: int = 15) -> None:
        # self.scheduler = BlockingScheduler(executors={'default': AsyncIOExecutor()}, 
        #                                   job_defaults={'misfire_grace_time': 10, 'max_instances': 5})
        self.scheduler = BlockingScheduler(job_defaults={'misfire_grace_time': 10, 'max_instances': 5})
        self.interval = interval
        self.job_queue = Queue()
        self.scheduler.add_listener(self.listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def run_forever(self) -> None:
        """Run the scheduler indefinitely"""
        logger.info("Starting the scheduler.")
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
        if event.exception:
            logger.error(f"Job {event.job_id} raised an exception: {event.exception}")
        else:
            logger.info(f"Job {event.job_id} executed successfully.")

    def get_queue_length(self) -> int:
        """Return the number of jobs in the queue"""
        return self.job_queue.qsize()

