import requests

class DataManager:
    def __init__(self):
        self.batch_data = []

    def add_to_batch(self, data):
        self.batch_data.append(data)

    def send_batch_data(self):
        print('Data has been sent to the backend.')
        url = "http://localhost:8000/receive_data/weather"
        with requests.Session() as s:
            response = s.post(url, json=self.batch_data)
        self.batch_data = []

data_manager = DataManager()
