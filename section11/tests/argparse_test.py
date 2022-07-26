import argparse

store_name_parser = argparse.ArgumentParser()
store_name_arg = store_name_parser.add_argument("--name", "-n")
store_name = store_name_parser.parse_args().name
print(store_name)