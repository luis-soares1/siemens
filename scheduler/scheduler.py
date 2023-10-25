import os
from settings.config import get_settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from queue import Queue


class Scheduler():
    def __init__(self) -> None:
        self.scheduler = BlockingScheduler(job_defaults={'misfire_grace_time': 5})
        self.interval = get_settings().job_interval
        self.job_queue = Queue()
    # se um job falhar, adicionar de novo à queue, em primeiro lugar. Talvez utilizar deque
    def start(self) -> None:
        print(self.job_queue.qsize())
        try:
            while not self.job_queue.empty():
                fn, kwargs = self.job_queue.get()
                self.scheduler.add_job(fn, 'interval', seconds=self.interval, kwargs={**kwargs}, max_instances=5)
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()

    def enqueue_job(self, fn, kwargs) -> None:
        self.job_queue.put((fn, kwargs))
        
    def get_queue_length(self) -> int:
        return self.job_queue.qsize()

