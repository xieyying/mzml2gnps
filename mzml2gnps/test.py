import os



def path_check(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory {path} created successfully.")
    else:
        print(f"Path {path} already exists.")