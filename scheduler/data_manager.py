from settings.config import settings
from utils.logging import logger
import requests


class DataManager:
    def __init__(self):
        self.batch_data = []

    def add_to_batch(self, data: dict) -> None:
        self.batch_data.append(data)

    def send_batch_data(self) -> None:
        response = ""
        url = f"http://{settings.host}:{settings.port}/receive_data/weather"
        with requests.Session() as s:
            response = s.post(url, json=self.batch_data)
        self.batch_data = []

        logger.info(
            f"Data has been sent. Got the following response back: {response}")


data_manager = DataManager()
