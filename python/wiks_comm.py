# -*- coding: utf-8 -*-

import os
import logging.handlers
import logging


def setup_logger(logger_name,
                 log_file,
                 level=logging.INFO):
    """

    przykład użycia:
    log_main = setup_logger('main', os.path.join(log_directory, 'log_.txt'))

    :param logger_name:
    :param log_file:
    :param level:
    :return:
    """
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d  %(levelname)-8s  %(name)-15s  %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = logging.handlers.RotatingFileHandler(log_file,
                                                        maxBytes=1000000,
                                                        backupCount=3)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(file_handler)
    l.addHandler(stream_handler)
    return l


def logger_create_dir_var_log_(sub_path=None):
    """
    jeśli brak to utwórz katalog w VAR LOG
    :return:
    """
    log_directory = '/var/log/'
    if sub_path:
        log_directory += sub_path
        # os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  # script directory
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
    return log_directory
