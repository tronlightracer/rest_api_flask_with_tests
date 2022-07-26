import json
import requests
from pprint import pprint
import argparse

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

access_token = login.json()['access_token']
header2 = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}

def test_cleanup():
    got = requests.get(
        r_bin + "get",
    )

    posted = requests.post(
        r_bin + "post",
        headers=header1,
        json={"post": "test"}
    )

    deleted = requests.delete(
        r_bin + "delete",
        headers=header1
    )
    print("""
    These responses are to test the environment to make sure it can do requests
    The responses are in the order of get, post and delete
        """)
    print(got)
    print(posted)
    print(deleted)

    #return got.json(), posted.json(), deleted.json()

test = test_cleanup()

# def advance_cleanup(name):

#     got = requests.get(
#     my_app + "stores"
#         )
#     print("got", got)
#     print(got.json()['stores'])
#     if got.json()['stores'] == None:
#         print("the list is empty")
#     store_dict = got.json()
#     for i in store_dict['stores']:
#         for v in i.values():
#             if v == name:
#                 deleted = requests.delete(
#                     my_app + f"store/{name}",
#                     headers=header2,
#                 )
#                 print("deleted", deleted)
#                 return deleted.json()
                
#             else:
#                 posted = requests.post(
#                     my_app + f"store/{name}",
#                     headers=header2,
#                 )
#                 print("posted", posted)
#                 return posted.json()
    

# cleanup = advance_cleanup(store_name)

def advance_cleanup(name):

    got = requests.get(
    my_app + "stores"
        )
    print("got", got)
    #print(got.json()['stores'])
    if not got.json()['stores']:
        posted = requests.post(
            my_app + f"store/{name}",
            headers=header2,
        )
        print("posted json:", posted.json())
        return posted
    else:
        for i in got.json()['stores']:
           for v in i.values():
            if v == name:
                deleted = requests.delete(
                    my_app + f"store/{name}",
                    headers=header2,
                ) 
                print("deleted json:", deleted.json())
                return deleted
    

# cleanup = advance_cleanup(store_name)

def advance_cleanup2(name):
    
    access_token = login.json()['access_token']
    header2 = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}

    got = requests.get(
    my_app + "stores"
    )
    print("got", got)
    print(got.json())

    if not got.json()['stores']:
        posted = requests.post(
            f"{my_app}/store/{name}",
            headers=header2,
        )
        print(f"post json data: {posted.json()}")
        return posted
    else:
        for store in got.json()['stores']:
            for v in store.values():
                if v == name:
                    deleted = requests.delete(
                        f"{my_app}/store/{name}",
                        headers=header2,
                    )
                    print(f"deleted json: {deleted.json()}")
                    return deleted
                else:
                    deleted = requests.delete(
                        f"{my_app}/store/{name}",
                        headers=header2,
                    )
                    print(f"deleted json: {deleted.json()}")
                    return deleted



cleanup = advance_cleanup2(store_name)

# get_stores = requests.get(
#     my_app + "stores"
# )
# print(get_stores.json())


# store_post = requests.post(
#     my_app + f"store/{store_name}",
#     #json={"stores": ['store1']},
#     headers=header2,
# )

# store_del = requests.post(
#     my_app + f"store{store_name}",
#     headers=header2,
# )

# print(store_post)
# print(store_del)
# pprint(store_post.json())