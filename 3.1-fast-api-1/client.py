import requests

# response = requests.post(
#     "http://127.0.0.1:8888/v1/advertisement",
#     json={
#         "title": "title",
#         "description": "description",
#         "price": 1000,
#         'author': 'user_1'
#     }
# )
# print(response.status_code)
# print(response.json())


response = requests.get("http://127.0.0.1:8888/v1/advertisement?title")
print(response.status_code)
print(response.json())

# response = requests.patch("http://127.0.0.1:8888/v1/advertisement/1", json={
#     "done": True,
#     'title': 'new_title'
# })
# print(response.status_code)
# print(response.json())



# response = requests.delete("http://127.0.0.1:8888/v1/advertisement/2",)
# print(response.status_code)
# print(response.json())