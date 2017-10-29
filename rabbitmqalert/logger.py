import logging
from logging import handlers
from sys import stdout

LOGGING_PATH = "/var/log/rabbitmq-alert/rabbitmq-alert.log"


class Logger:
    @staticmethod
    def log(severity, message):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        rotate_handler = handlers.TimedRotatingFileHandler(
            filename=LOGGING_PATH,
            when="midnight"
        )
        rotate_handler.suffix = "%Y%m%d"
        rotate_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(rotate_handler)

        stoud_handler = logging.StreamHandler(stdout)
        stoud_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s - %(asctime)s"))
        logger.addHandler(stoud_handler)

        if severity == logging.DEBUG:
            logger.debug(message)
        elif severity == logging.INFO:
            logger.info(message)
        elif severity == logging.WARN or severity == logging.WARNING:
            logger.warn(message)
        elif severity == logging.ERROR:
            logger.error(message)
        elif severity == logging.CRITICAL:
            logger.critical(message)

    def debug(self, message):
        self.log(logging.DEBUG, message)

    def info(self, message):
        self.log(logging.INFO, message)

    def warn(self, message):
        self.log(logging.WARN, message)

    def error(self, message):
        self.log(logging.ERROR, message)

    def critical(self, message):
        self.log(logging.CRITICAL, message)
