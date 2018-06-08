import logging

_log_level = logging.INFO
_log_format = "[%(asctime)s][%(filename)s][line:%(lineno)d]" \
              "[%(levelname)s] %(message)s"

logger = logging.getLogger("EventNotificator")
logger.setLevel(_log_level)
sh = logging.StreamHandler()
sh .setFormatter(logging.Formatter(_log_format))
logger.addHandler(sh)


def set_log_filepath(filepath):
    fh = logging.FileHandler(filepath, mode='a')
    fh.setFormatter(logging.Formatter(_log_format))
    logger.addHandler(fh)
    logger.removeHandler(sh)

