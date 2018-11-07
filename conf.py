# -*- coding: utf-8 -*-

import logging

FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG


LOG = {
        'log_level': INFO,
        'log_path': 'log.log',
      }


SPIDER = {
           'max_retry': 5,
           'timeout': 5,
         }


PIPELINES = []

EXCEPTIONS = []

EMAIL = {
        'host': None,
        'port': 0,
        'use_ssl': False,
        'usr': '',
        'pwd': '',
        'Subject': None,
        'To': None,
        'From': None
        }

DATABASE = {
             'mongodb': {'mongodb_connect_string': '',
                         'database': '',
                         'collection': ''}
             'mysql': {'mysql_connect_string': ''}
           }
