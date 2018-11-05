# -*- coding: utf-8 -*-

import logging

FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG


LOG = {
        'log_level': INFO,
        'log_path': 'spider_log.log',
      }


SPIDER = {
           'max_retry': 5,
           'timeout': 5,
         }


PIPELINES = []

EXCEPTIONS = []
