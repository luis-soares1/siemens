import os
import requests
import json

class ApiService:
    def __init__(self) -> None:
        self.url = ""
        self.api_key = ""
        self.load_env_variables()
    
    def load_env_variables(self) -> bool:
        self.url = os.environ.get('API_URL')
        self.api_key = os.environ.get('API_KEY')
        if not self.url:
            raise Exception("API URL not available. Please insert it in the .env file")
        if not self.api_key:
            raise Exception("API Key not available. Please insert it in the .env file")

    def get_current_weather(self):
        try:
            data = requests.get(f"{self.url}/weather?lat=38.7320286&lon=-9.217414&appid={self.api_key}")       
            print(data.text)
        except:
            print('couldnt handle request.')
