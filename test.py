import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"name": "ishwar", "views": 300000, "likes": 1000},
    {"name": "pranay", "views": 200000, "likes": 100000},
    {"name": "bhaiyu", "views": 150000, "likes": 20000},
    ]

data_to_update = {
    "likes": 300000
}

# response = requests.get(BASE + "helloworld/ishwar")
# response = requests.put(BASE + "video/1", json=data)

# if response.status_code == 201:
    # print("PUT request successful.")
    # print(response.json())
# else:
    # print(f"PUT request failed with status code: {response.status_code}")

# input()
# 
for i in range(len(data)):
    response = requests.put(BASE + "video/"+str(i), json=data[i])
    if response.status_code == 201:
        print("PUT request successful.")
        print(response.json())
    else:
        print(f"PUT request failed with status code: {response.status_code}")

input()

response = requests.delete(BASE + "video/0")
if response.status_code == 204:
    print("DELETE request successful.")
    print(response)
else:
    print(f"DELETE request failed with status code: {response.status_code}")

input()

response = requests.get(BASE + "video/1")
if response.status_code == 200:
    print("GET request successful.")
    print(response.json())
else:
    print(f"GET request failed with status code: {response.status_code}")

input()

response = requests.patch(BASE + "video/1", json=data_to_update)
if response.status_code == 200:
    print("UPDATE request successful.")
    print(response.json())
else:
    print(f"UPDATE request failed with status code: {response.status_code}")
