import requests
from pprint import pprint
import argparse

import click

store_name_parser = argparse.ArgumentParser()
store_name_arg = store_name_parser.add_argument("--name")
store_name = store_name_parser.parse_args().name

my_app = "http://127.0.0.1:3200/"
r_bin = "https://httpbin.org/"
header1 = {"Content-Type": "application/json"}
usern = "123"
passw = "123"

register = requests.post(
    my_app + "register",
    json={"username": usern, "password": passw},
    headers=header1,
)

login = requests.post(
    my_app + "login",
    json={"username": usern, "password": passw},
    headers=header1,
)

# pprint(login.json())

access_token = login.json()['access_token']
header2 = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}

store_post = requests.post(
    my_app + f"store/{store_name}",
    #json={"stores": ['store1']},
    headers=header2,
)

store_del = requests.post(
    my_app + f"store{store_name}",
    headers=header2,
)

print(store_post)
print(store_del)
# pprint(store_post.json())