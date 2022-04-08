#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: log.py
import logging
from typing import Optional

import sentry_sdk
from rich.logging import RichHandler
from sentry_sdk.integrations.executing import ExecutingIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.pure_eval import PureEvalIntegration

from neorg import constants

TRACE_LEVEL = 5


class CustomLogger(logging.Logger):
    """Custom Logger, initialized with rich handler"""

    def __init__(self, name: Optional[str], level: logging = logging.NOTSET):
        super().__init__(name, level)
        self.addHandler(RichHandler())

    def trace(self, msg: Optional[str], *args, **kwargs) -> None:
        """Trace Level message Custom for this logger"""
        if self.isEnabledFor(TRACE_LEVEL):
            self.log(TRACE_LEVEL, msg, *args, **kwargs)


def get_logger(name: Optional[str] = None) -> CustomLogger:
    """Return a logger with the given name. Which tends to be done by
    get_logger(__name__) in most cases.

    Parameters
    ----------
    name : Optional[str]
        Name of instance / module

    Returns
    -------
    CustomLoggerLogger
        CustomerLoger
    """
    return CustomLogger(name)  # create a logger with the name of the module


def setup() -> None:
    """ setup file for logger - initalises level, format  and its own trace """
    logging.TRACE = TRACE_LEVEL
    logging.addLevelName(TRACE_LEVEL, "TRACE")
    logging.setLoggerClass(CustomLogger)

    root_log = get_logger()

    format_string = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    logging.Formatter(format_string)
    root_log.setLevel(logging.INFO)
    _set_trace_loggers()


def _set_trace_loggers() -> None:
    """ set the loggers to trace level """
    level_filter = logging.Filter()
    if level_filter.filter(logging.makeLogRecord({'levelno': TRACE_LEVEL})):
        get_logger().setLevel(TRACE_LEVEL)


def setup_sentry() -> None:
    """ God Mode logger, helps find issues that are not caught by the logger """
    sentry_sdk.init(
        dsn=f"https://{constants.SENTRY}",
        auto_session_tracking=True,
        traces_sample_rate=1.0,
        integrations=[
            LoggingIntegration(level=logging.DEBUG, event_level=logging.WARNING),
            PureEvalIntegration(),
            ExecutingIntegration()
        ],
    )

    sentry_sdk.capture_exception()
