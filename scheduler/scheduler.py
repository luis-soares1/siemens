from apscheduler.schedulers.asyncio import AsyncIOScheduler
from queue import Queue


# se um job falhar, adicionar de novo à queue, em primeiro lugar. Talvez utilizar deque
class Scheduler():
    def __init__(self) -> None:
        self.scheduler: AsyncIOScheduler  = AsyncIOScheduler()
        self.interval: int = 3600 # Importar da .env
        self.job_queue: Queue = Queue()

    def init_scheduler(self):
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()
    
    def add_job(self, fn, interval):
        self.job_queue.put(fn)
    
    
    
    
