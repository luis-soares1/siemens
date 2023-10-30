from common.settings.config import script_settings
from common.utils.logging import logger
import requests


class DataManager:
    def __init__(self):
        self.batch_data = []

    def add_to_batch(self, data: dict) -> None:
        self.batch_data.append(data)

    def send_batch_data(self) -> None:
        response = ""
        url = f"http://{script_settings.host}:{script_settings.port}/receive_data/weather"
        print(len(self.batch_data), 'TAMANHO DO BATCH')
        with requests.Session() as s:
            response = s.post(url, json=self.batch_data)
        self.batch_data = []

        logger.info(
            f"Data has been sent. Got the following response back: {response}")


data_manager = DataManager()
