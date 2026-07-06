import os
class Logger:
    @staticmethod
    def log(message):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir,"invalid_log.txt")
        with open(filename,"a") as file:
            file.write(message + "\n")