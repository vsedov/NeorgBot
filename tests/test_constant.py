import unittest

from neorg import constants


class ConstantsTests(unittest.TestCase):
    """Test Constants"""

    def test_file_type_hint(self):

        instaces = [list, list[str], int, str, float, bool, type(None)]
        for key, value in constants.__dict__.items():
            if key.isupper():
                self.assertIn(type(value), instaces)

    def test_env_variables(self):
        token = constants.TOKEN
        self.assertIsInstance(token, str)
        self.assertIsNotNone(token)
