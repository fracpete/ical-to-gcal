import logging
import os


_logger = None


def logger() -> logging.Logger:
    """
    Return the logger to use.

    :return: the logger
    :rtype: logging.Logger
    """
    global _logger
    if _logger is None:
        _logger = logging.getLogger("itg.api.core")
    return _logger


def get_default_config_dir():
    """
    Returns the default config dir.

    :return: the default config file
    :rtype: str
    """
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".config", "otg")
    if not os.path.exists(config_dir):
        logger().info("Creating dir: %s" % config_dir)
        os.makedirs(config_dir)
    return config_dir
