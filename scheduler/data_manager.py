import requests

class DataManager:
    def __init__(self, batch_size: int = 10):
        self.batch_data = []
        self.batch_size = batch_size

    def add_to_batch(self, data):
        self.batch_data.append(data)
        if len(self.batch_data) >= self.batch_size:
            self.send_batch_data()

    def send_batch_data(self):
        url = "http://localhost:8000/receive_data/weather"
        with requests.Session() as s:
            response = s.post(url, json=self.batch_data)
        self.batch_data = []

data_manager = DataManager()
