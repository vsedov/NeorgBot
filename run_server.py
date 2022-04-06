#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © Vivian Sedov
#
# File Name: run_server.py
from sys import path


path.append("src/main/python/")

def main() -> None:
    #  TODO(vsedov) (01:43:33 - 05/04/22): Change load, and have better debugs, also create test case
    __import__("hosting").FlaskThread("127.0.0.1", 8000).start()

if __name__ == "__main__":
    main()
