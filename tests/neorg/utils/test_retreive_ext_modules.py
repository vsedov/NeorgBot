#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: test_retreive_ext_modules.py

import unittest

from neorg.log import get_logger
from neorg.utils import extensions

log = get_logger(__name__)


class TestUtilCogClass(unittest.TestCase):
    """Test the ext loading class, which is a subclass of the builtin, it loads cogs based on filestructure."""

    def test_unqualify(self):
        """Test the unqualify function, which removes the cog name from the extension name."""
        self.assertEqual(extensions.unqualify('neorg.utils.extensions'), 'extensions')
        self.assertEqual(extensions.unqualify('neorg.utils.extensions.unqualify'), 'unqualify')
        self.assertEqual(extensions.unqualify('neorg.utils.extensions.unqualify.unqualify'), 'unqualify')

    def test_walk_extensions(self):
        """Test the walk_extensions function, which walks the extension directory and returns a list of cog names."""
        walk = extensions.walk_extensions()
        frozen_set = list(frozenset(walk))
        self.assertGreater(len(frozen_set), 2)
        self.assertIn('neorg.ext.help_channel.help', frozen_set)
        self.assertIn('neorg.ext.neorg_wiki.neorg_cmds', frozen_set)

    def test_global_extension(self):
        """Test the global_extension function, which returns a list of cog names."""
        ext = extensions.EXTENSIONS
        self.assertIn('neorg.ext.help_channel.help', ext)
        self.assertIn('neorg.ext.neorg_wiki.neorg_cmds', ext)
        self.assertGreater(len(ext), 2)
        self.assertIsInstance(ext, frozenset)

    def test_find_extension(self):
        """Test the find_extension function, which returns a list of cog names."""
        ext = {
            "help": "neorg.ext.help_channel.help",
            "neorg_cmds": "neorg.ext.neorg_wiki.neorg_cmds"
        }
        for key, value in ext.items():
            self.assertEqual(extensions.find_extension(key), value)
