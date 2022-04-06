#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: test_retreive_cog_modules.py

import unittest

from neorg.utils import extensions


class TestUtilCogClass(unittest.TestCase):

    def test_unqualify(self):
        # test a unqualified name given a qualified module/packagename
        self.assertEqual(extensions.unqualify('neorg.utils.extensions'), 'extensions')
        self.assertEqual(
            extensions.unqualify('neorg.utils.extensions.unqualify'), 'unqualify')
        self.assertEqual(
            extensions.unqualify('neorg.utils.extensions.unqualify.unqualify'),
            'unqualify')

    def test_walk_extensions(self):
        walk = extensions.walk_extensions()
        frozen_set = list(frozenset(walk))
        self.assertGreater(len(frozen_set), 2)
        self.assertIn('neorg.cogs.help_channel.help', frozen_set)
        self.assertIn('neorg.cogs.utils.neorg_cmds', frozen_set)

    def test_global_extension(self):
        ext = extensions.EXTENSIONS
        self.assertIn('neorg.cogs.help_channel.help', ext)
        self.assertIn('neorg.cogs.utils.neorg_cmds', ext)
        self.assertGreater(len(ext), 2)
        self.assertIsInstance(ext, frozenset)
