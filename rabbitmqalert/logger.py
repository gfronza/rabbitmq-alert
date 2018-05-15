import logging
from logging import handlers
from sys import stdout

LOGGING_PATH = "/var/log/rabbitmq-alert/rabbitmq-alert.log"


class Logger:

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        rotate_handler = handlers.TimedRotatingFileHandler(
            filename=LOGGING_PATH,
            when="midnight"
        )
        rotate_handler.suffix = "%Y%m%d"
        rotate_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        self.logger.addHandler(rotate_handler)

        stoud_handler = logging.StreamHandler(stdout)
        stoud_handler.setFormatter(logging.Formatter("%(asctime)s: %(levelname)s - %(message)s"))
        self.logger.addHandler(stoud_handler)

    def get_logger(self):
        return self.logger
