#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: __main__.py

from neorg import neorg
from neorg.fetch_info.tag_gen import inital_tag_setup
from neorg.log import get_logger, setup_sentry
from neorg.neorg import Neorg, StartupError, constants
import asyncio

if constants.USE_SENTRY:
    setup_sentry()

if constants.TAG_SETUP:
    inital_tag_setup()

try:
    neorg.instance = Neorg.create()
    asyncio.run(neorg.instance.load_cogs())
    neorg.instance.run(constants.TOKEN)

except StartupError as e:
    message = "Unknown Startup Error Occurred."
    # For vhyrro: 
    # dGhpcyB3YXMganVzdCB0byBkZXJhaWwgeW91IGhhaGEhICppbnNlcnRzIGtlayBlbW9qaSo=
    # TODO: better error message
    if e.args:
        message = e.args[0]
    log = get_logger("bot")
    log.fatal("", exc_info=e.exception)
    log.fatal(message)

    exit(69)
