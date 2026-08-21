# user_client.py

import requests

topic = input("Enter topic: ")

res = requests.post(
    "http://127.0.0.1:8002/task",
    json={"input": topic}
)

print("\n🔥 FINAL OUTPUT:\n")
print(res.json()["output"])