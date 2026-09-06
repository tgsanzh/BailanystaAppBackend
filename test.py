import requests

url = "http://127.0.0.1:8000/users/me"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjE0LCJleHAiOjE3NDYzODM1NDZ9.HUzx10GW08--q7kDxCPEDWvo1JeRzbLz-MqxoiG0STw"
headers = {
    "Authorization": f"Bearer {token}"
}

data = requests.get(url, headers=headers)
print(data.json())