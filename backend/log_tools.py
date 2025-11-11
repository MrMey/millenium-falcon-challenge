import logging


def set_all_loggers_level(level):
    logging.root.setLevel(level)

    for name in logging.root.manager.loggerDict.keys():
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.debug(f"Set level of logger '{name}' to {logging.getLevelName(level)}")
