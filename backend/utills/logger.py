from ..models.log import Log
import datetime

from ..extensions import session

class Logger:
    def __init__(self, session_id):
        self.session_id = session_id

    def log(self, message, level):
        # Truncate message to prevent DB errors (logs table message column limit)
        truncated_message = message[:500] if len(message) > 500 else message
        
        log = Log(
            message=truncated_message,
            level=level,
            session_id=self.session_id
        )

        print(f"{datetime.datetime.now()} - {level} - {message}")

        session.add(log)
        session.commit()

    def log_error(self, message):
        self.log(message, 3)

    def log_warning(self, message):
        self.log(message, 2)

    def log_info(self, message):
        self.log(message, 1)