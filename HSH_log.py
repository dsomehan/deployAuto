# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     HSH_log.py
   Description :
   Author :       HSH
   date：          2017/11/1
-------------------------------------------------
   Change Activity:
                   2017/11/1:
-------------------------------------------------
"""
__author__ = 'HSH'

import logging
import configparser

cf = configparser.ConfigParser()
cf.read('HSH_log.conf', encoding='UTF-8')

logging.basicConfig(**cf['basicConfig'])

critical = logging.critical
error = logging.error
warn = logging.warning
info = logging.info
debug = logging.debug

