import requests
from pprint import pprint
import argparse

store_name_parser = argparse.ArgumentParser()
store_name_arg = store_name_parser.add_argument("--store_name")
item_name_arg = store_name_parser.add_argument("--item_name")
store_name = store_name_parser.parse_args().store_name
item_name = store_name_parser.parse_args().item_name

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



def advance_cleanup(name, item):
    
    access_token = login.json()['access_token']
    header2 = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}

    got = requests.get(
    my_app + "stores"
    )
    print("got", got)
    print(got.json())

    get_items = requests.get(
        my_app + "items"
    )
    print(get_items)

    if not got.json()['stores']: #and not get_items.json():
        posted = requests.post(
            f"{my_app}/store/{name}",
            headers=header2,
        )
        print(f"post json data: {posted.json()}")
        assert posted.json() == {'id': 1, 'name': store_name, 'items': []}
        
        item_post = requests.post(
            f"{my_app}/item/{item}",
            headers=header2,
            json={"username": usern, "password": passw, "price": 22, "store_id": 1}
        )
        print(f"post item json data: {item_post.json()}")
        item1 = {'id': 1, 'name': item, 'price': 22.0, 'store_id': 1}
        assert item_post.json() == item1

    else:
        for v in got.json()['stores'][0].values():
            if v == name:
                deleted = requests.delete(
                    f"{my_app}/store/{name}",
                    headers=header2,
                )
                print(f"deleted json: {deleted.json()}")
                assert deleted.json() == {'message': 'Store deleted'}
                return deleted
            else:
                posted2 = requests.post(
                    f"{my_app}/store/{name}",
                    headers=header2,
                )
                print(f"posted json: {posted2.json()}")
                assert {'id': 1, 'name': 'store1', 'items': [{'id': 1, 'name': item, 'price': 22.0, 'store_id': 1}]}
                return posted2

print(advance_cleanup(store_name, item_name))