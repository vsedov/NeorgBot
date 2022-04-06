import unittest

from neorg.fetch_info.fetch_from_awesome import ReadAwesome, weak_lru


class TestMessages(unittest.TestCase):

    def test_fetch_info_lsp(self):
        message_lsp = ReadAwesome().fuzzy('lsp')
        # format message first
        for name, desc in message_lsp.items():
            # check if either name or desc contains lsp
            self.assertTrue(
                name.lower().find('lsp') != -1 or desc.lower().find('lsp') != -1)

        self.assertGreater(len(message_lsp), 2)

    def test_null_case(self):
        message_null = ReadAwesome().fuzzy('')
        self.assertEqual(message_null, {})

    def test_weak_lur(self):

        @weak_lru(maxsize=128, typed=False)
        def func(self, *args, **kwargs):
            return self.__class__.__name__

        class A:

            def __init__(self):
                self.a = 1

            @func
            def __call__(self):
                return self.a

        self.assertEqual(func(A()), 'A')

    def test_get_header(self):
        diction = ReadAwesome().get_from_header()
        self.assertGreater(len(diction), 20)

    def test_contains_atleast_one_link(self):
        diction = ReadAwesome().get_from_header()
        for x in diction.values():
            self.assertIsInstance(x, dict)
            self.assertIn('link', x)
            self.assertIn('desc', x)
            self.assertIsInstance(x['link'], str)
            self.assertIsInstance(x['desc'], str)
            self.assertGreater(len(x['link']), 0)
            self.assertGreater(len(x['desc']), 0)
