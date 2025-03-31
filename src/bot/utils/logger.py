import datetime

class Logger:

    def __init__(self, name_service: str):
        self.name = name_service

    def log(self, message: str):
        now = datetime.datetime.now()
        print(f"[{self.name}] - {now} - {message}")