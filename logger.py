# -*- coding: utf-8 -*-
import logging
from datetime import datetime as dt

def get_logger():
    """ 配置 logger """
    logger = logging.getLogger('sms_post')
    logger.setLevel(logging.DEBUG)
    log_filename = "sms_post_log_%s-%s-%s" % (dt.now().year, dt.now().month, dt.now().day)
    log_filename += '.log'
    with open(log_filename, 'w+'):
    	file_handler = logging.FileHandler(log_filename)
    	file_handler.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(ch)

    return logger

Logger = get_logger()
