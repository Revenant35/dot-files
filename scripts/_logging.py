import logging
import sys


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    message_format = "=> %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + message_format + reset,
        logging.INFO: grey + message_format + reset,
        logging.WARNING: yellow + message_format + reset,
        logging.ERROR: red + message_format + reset,
        logging.CRITICAL: bold_red + message_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("DotfileInstaller")
logger.setLevel(logging.DEBUG)

_info_handler = logging.StreamHandler(sys.stdout)
_info_handler.setLevel(logging.DEBUG)
_info_handler.addFilter(lambda record: record.levelno <= logging.INFO)
_info_handler.setFormatter(CustomFormatter())

_error_handler = logging.StreamHandler(sys.stderr)
_error_handler.setLevel(logging.DEBUG)
_error_handler.addFilter(lambda record: record.levelno > logging.INFO)
_error_handler.setFormatter(CustomFormatter())

logger.addHandler(_info_handler)
logger.addHandler(_error_handler)
