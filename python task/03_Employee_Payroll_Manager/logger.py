
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log_error(message):
    filename = os.path.join(BASE_DIR, "errors.log")
    with open(filename,"a") as file:
        file.write(message + "\n")

