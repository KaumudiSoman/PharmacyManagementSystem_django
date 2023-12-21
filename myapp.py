import requests

url = "http://127.0.0.1:8000/users/"
headers = {"Authorization": "Token 69bc2c1e87ef6a1baa6d679e314b8620f526d7a1"}

response = requests.get(url, headers=headers)


print(response.status_code)
print(response.json())