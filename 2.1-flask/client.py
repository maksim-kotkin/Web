import requests


response = requests.post(
    'http://127.0.0.1:5000/adv/',
    json={'owner_id': 1, 'title': 'guhreouhgo[r]frgijp','description': 'pf[sokg][[]',},

                                                     
)
# response = requests.post(
#     'http://127.0.0.1:5000/user/',
#     json={'username': 'user_555', 'email': 'kkkk@mail.ru','password': 'phje4pifc',},

                                                     
# )
# response = requests.patch(
#     'http://127.0.0.1:5000/user/6',
#          json={'name': 'name3', 'password':'new_1423'}                                      
# )

# print(response.status_code)
# print(response.json())
# response = requests.delete(
#     'http://127.0.0.1:5000/adv/3',
                                                     
# )

# response = requests.get(
#     'http://127.0.0.1:5000/adv/3',
                                                     
# )
print(response.status_code)
print(response.json())