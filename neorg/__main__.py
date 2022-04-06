#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: __main__.py

import aiohttp
import constants
from log import get_logger, setup_sentry

import neorg
from neorg import Neorg, StartupError

setup_sentry()

try:
    neorg.instance = Neorg.create()
    neorg.instance.load_cogs()
    neorg.instance.run(constants.TOKEN)

except StartupError as e:
    message = "Unknown Startup Error Occurred."
    if isinstance(e.exception,
                  (aiohttp.ClientConnectorError, aiohttp.ServerDisconnectedError)):
        message = "Could not connect to site API. Is it running?"
    elif isinstance(e.exception, OSError):
        message = "Could not connect to Redis. Is it running?"

    log = get_logger("bot")
    log.fatal("", exc_info=e.exception)
    log.fatal(message)

    exit(69)
