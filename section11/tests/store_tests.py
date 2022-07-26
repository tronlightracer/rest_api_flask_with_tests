from requests import delete, get, post

my_app = "http://127.0.0.1:3200/"
r_bin = "https://httpbin.org/"
header1 = {"Content-Type": "application/json"}
usern = "rustikk"
passw = "123"


post_test = post(
    r_bin + "post",
    data={"username": usern, 'password': passw})


register = post(
    my_app + "register",
    json={"username": usern, "password": passw},
    headers=header1,
)

login = post(
    my_app + "login",
    json={"username": usern, "password": passw}
)

access_token = login.json()['access_token']

header2 = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}

store_get = get(
    my_app + "stores",
)

# store_post = post(
#     my_app + "stores",
#     json={"stores":}
# )

# def assert_status_codes():
#     assert post_test == "<Response [200]>"
#     assert register == "<Response [201]>"
#     assert login == "<Response [200]>"
#     assert store_get == "<Response [200]>"

# run_tests = assert_status_codes

# print("httpbin post test:", post_test)
# print(register)
# print(login)
# print(store_get)

