import os
import requests

class ApiService:
    def __init__(self) -> None:
        self.url = ""
        self.api_key = ""
    
    def load_env_variables(self) -> bool:
        self.url = os.environ.get('API_URL')
        self.api_key = os.environ.get('API_KEY')
        if not self.url:
            raise Exception("API URL not available. Please insert it in the .env file")
        if not self.api_key:
            raise Exception("API Key not available. Please insert it in the .env file")

    def get_current_weather(self, lat, lon):
        try:
            data = requests.get(f"{self.url}/weather?lat={lat}&lon={lon}&appid={self.api_key}")       
        except:
            print('couldnt handle request.')

    