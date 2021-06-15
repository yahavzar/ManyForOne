import logging

def setup_logger(name, level=logging.DEBUG, formatter=None, log_path=None):
    """Return a logger with a default ColoredFormatter."""
    try:

        logging.addLevelName(51, 'SUCCESS')
        logging.addLevelName(22, 'PROCESS')
        if not formatter:
            formatter = logging.Formatter('%(levelname)s - %(name)-5s - %(message)s')
        if log_path:
            handler = logging.FileHandler(log_path, 'a', 'utf-8')
        else:
            handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.addHandler(handler)
        logger.propagate = False
        logger.setLevel(level)
        return logger

    except:
        print("ERROR - failed to create logger %s" % name)
