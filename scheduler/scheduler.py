from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.executors.pool import ThreadPoolExecutor
from queue import Queue
from typing import Callable
from common.settings.script_config import script_settings
from common.utils.logging import logger


class JobScheduler:
    """Scheduler to manage and execute jobs at specified intervals."""

    def __init__(
        self,
        max_instances: int = 1,
        cycle_callback: Callable[[],
                                 None] = lambda: None) -> None:

        self.executors = {
            'default': ThreadPoolExecutor(max_instances)
        }

        self.job_defaults = {
            'misfire_grace_time': script_settings.job_interval,
            'max_instances': max_instances
        }
        self.current_jobs_count = 0
        self.total_jobs_count = 0
        self.cycle_callback = cycle_callback
        self.scheduler = BlockingScheduler(
            job_defaults=self.job_defaults,
            executors=self.executors
        )
        self.jobs_queue = Queue()
        self.scheduler.add_listener(
            self._job_event_listener,
            EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def run(self) -> None:
        """Start the scheduler."""
        logger.info("Starting the scheduler.")
        self.total_jobs_count = self.jobs_queue.qsize()
        self._schedule_all_jobs_in_queue()
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()
            logger.info("Scheduler has been shut down.")

    def enqueue_job(self, fn: Callable, kwargs: dict) -> None:
        """Add a job to the scheduler's queue."""
        self.jobs_queue.put((fn, kwargs))

    def _schedule_all_jobs_in_queue(self) -> None:
        """Schedule all jobs present in the queue."""
        while not self.jobs_queue.empty():
            fn, kwargs = self.jobs_queue.get()
            self.scheduler.add_job(
                fn,
                'interval',
                seconds=script_settings.job_interval,
                kwargs=kwargs)

    def _job_event_listener(self, event) -> None:
        """Listener for job events."""
        self.current_jobs_count += 1

        if event.exception:
            logger.error(
                f"Job {event.job_id} raised an exception: {event.exception}")
        else:
            logger.info(f"Job {event.job_id} executed successfully.")

        if self._has_completed_cycle():
            self.current_jobs_count = 0
            self.cycle_callback()

    def _has_completed_cycle(self) -> bool:
        """Check if all jobs in the cycle have been executed."""
        return self.current_jobs_count == self.total_jobs_count
