import requests

data = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=38.7441844&lon=-9.2421374&appid=d2885c3159b8754fffbec7bfd235154c")
print(data.text)