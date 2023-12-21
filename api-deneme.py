import requests

url = "http://0.0.0.0:8000/giris"  # Replace with the actual URL
data = {"kadi": "iktuavarac2", "sifre": "123456"}  # Replace with your request payload

response = requests.post(url, json=data)

