#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © Vivian Sedov
#
# File Name: hosting.py
from threading import Thread

from flask import Flask

app = Flask('')

class FlaskThread:

    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        self.host = host
        self.port = port

    @app.route('/')
    def main():
        return "Your bot is ready"

    def run(self):
        app.run(host=self.host, port=self.port, debug=True, use_reloader=False)

    def start(self):
        setup = Thread(target=self.run)
        setup.start()
        return setup

    def __enter__(self):
        return self

    def stop(self):
        app.stop()
