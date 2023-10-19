from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

class ApiScheduler:
    def __init__(self) -> None:
        self.scheduler = 


def job(fn):
    print(fn(), f"Ive been printed at {datetime.now()}")
    