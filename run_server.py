#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: run_server.py
import logging
from sys import path

import pyinspect as pi
from rich.logging import RichHandler

path.append("src/main/python/")
root = logging.getLogger()
if root.handlers:
    for h in root.handlers:
        root.removeHandler(h)()

FORMAT = "%(message)s"
logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

def main() -> None:
    #  TODO(vsedov) (01:43:33 - 05/04/22): Change load, and have better debugs, also create test case
    __import__("hosting").FlaskThread("127.0.0.1", 8000).start()

if __name__ == "__main__":
    pi.install_traceback(enable_prompt=True)
    main()
