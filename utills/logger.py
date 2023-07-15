import datetime

class Logger:
    def __init__(self):
        self.logs = []

    
class Log:
    def __init__(self, message: str, level: int):
        self.message = message
        self.level = level
        self.timestamp = datetime.now()
