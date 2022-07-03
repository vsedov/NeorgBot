import unittest

import validators

from neorg.fetch_info.neovim_docs import NeovimDocs
from neorg.log import get_logger

log = get_logger(__name__)


class TestNeovimDocs(unittest.TestCase):
    """Test neovim doc search and search"""

    neovim_docs = NeovimDocs()

    def test_all_tags_not_none(self):
        """Test tags are present by checking if value is not Null"""
        tags = self.neovim_docs.get_all_tags()
        self.assertIsNotNone(tags)

    def test_fuzzy_search_tags(self):
        """Test fuzzy search tags"""
        tags = self.neovim_docs.fuzzy_search_tags("neovim", limit=10)
        self.assertIsNotNone(tags)
        self.assertTrue(len(tags) == 10)

        accurate_tag_lists = [("highlight-gui", 1), ("highlight-guifg", 1)]
        obsure_tag_lists = [("highlight guifg", 10), ("nvim-config", 4), ("lsp config", 5), ("highlights api", 10)]
        accurate_one_item_return_list = [("highlight-gui", 1)]

        def search(tag_list: list[str]):
            """Simple functino to parse a limit for each tag"""
            for tags, limit in tag_list:
                tag_link_list = self.neovim_docs.get_link(
                    self.neovim_docs.fuzzy_search_tags(search_term=tags, limit=limit))
                for url, tag_value in tag_link_list:
                    log.info(f"search item {tags} with url {url}, with {tag_value}")
                    self.assertTrue(validators.url(url))

        search(accurate_one_item_return_list)
        search(obsure_tag_lists)
        search(accurate_tag_lists)
