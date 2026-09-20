import logging
def setup_loggging(logger_name,logger_file):
    logger=logging.getLogger(logger_name)
    handler=logging.FileHandler(logger_file)
    format=logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(format)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
