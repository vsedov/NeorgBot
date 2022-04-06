#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: log.py
import logging
from typing import Optional

from neorg import constants
import sentry_sdk
from rich.logging import RichHandler
from sentry_sdk.integrations.logging import LoggingIntegration

TRACE_LEVEL = 5

class CustomedLogger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        self.addHandler(RichHandler())

    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(TRACE_LEVEL):
            self.log(TRACE_LEVEL, msg, *args, **kwargs)

def get_logger(name: Optional[str] = None) -> CustomedLogger:
    return CustomedLogger(name)  # create a logger with the name of the module

def setup() -> None:
    logging.TRACE = TRACE_LEVEL
    logging.addLevelName(TRACE_LEVEL, "TRACE")
    logging.setLoggerClass(CustomedLogger)

    root_log = get_logger()

    format_string = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    logging.Formatter(format_string)
    root_log.setLevel(logging.INFO)
    _set_trace_loggers()

def _set_trace_loggers() -> None:
    level_filter = logging.Filter()
    if level_filter.filter(logging.makeLogRecord({'levelno': TRACE_LEVEL})):
        get_logger().setLevel(TRACE_LEVEL)

# need to be called in __main__.py
#  HACK(vsedov) (11:34:23 - 05/04/22): Not sure if this works
def setup_sentry() -> None:
    sentry_sdk.init(
        dsn=f"https://{constants.SENTRY}",
        integrations=[
            LoggingIntegration(level=logging.DEBUG, event_level=logging.WARNING)
        ],
    )
