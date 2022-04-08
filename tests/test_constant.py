#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: test_constant.py
import unittest

from neorg import constants


class ConstantsTests(unittest.TestCase):
    """Test Constants"""

    def test_file_type_hint(self):
        """ Ensure everything in contant is type hinted. """
        instaces = [list, list[str], int, str, float, bool, type(None)]
        for key, value in constants.__dict__.items():
            if key.isupper():
                self.assertIn(type(value), instaces)

    def test_env_variables(self):
        """
        You need to have a token within your env for tests to pass.
        Mutable.
        """
        token = constants.TOKEN
        self.assertIsInstance(token, str)
        self.assertIsNotNone(token)
