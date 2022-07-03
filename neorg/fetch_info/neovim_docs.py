import sqlite3
from typing import Any, List, Tuple

from fuzzywuzzy import process

from neorg import constants
from neorg.log import get_logger

log = get_logger(__name__)


class NeovimDocs:
    """
    class for  neovim documentation: gets tags and use fuzzy search to find
    best matched item
    """

    def __init__(self):
        self.conn = sqlite3.connect(constants.DATABASE_PATH + "/tags.db")
        self.cursor = self.conn.cursor()
        self.all_tags = self.get_all_tags()
        self.tag_file = dict(list(map(lambda x: (x[1], x[0]), self.all_tags)))

    def get_all_tags(self) -> List[Any]:
        """Returna List of all tags that we can refer to. """
        return self.cursor.execute("SELECT * FROM tags").fetchall()

    def fuzzy_search_tags(self, search_term: str, limit: int = 1, cut_off_limit: int = 70) -> List[Any]:
        """Fuzzy search tags

        Parameters
        ----------
        search_term : str
            search term, can be an ambiguous string related to neovim or the item you want to search.
        limit : int
            limit , how many items do you want
        cut_off_limit : int
            how accurate should this be ? default is 70

        Returns
        -------
        List[Any]
            returna list of [(filename, tag)]
        """
        if limit == 1:
            search = process.extractOne(search_term, self.tag_file.keys(), score_cutoff=cut_off_limit)
            return [(self.tag_file[search[0]], search_term)]

        search = process.extractBests(search_term, self.tag_file.keys(), limit=limit, score_cutoff=cut_off_limit)
        log.info(search)
        return list(map(lambda x: (self.tag_file[x[0]], x[0]), search))

    def get_link(self, list_of_tags: List[Tuple[str, str]]) -> List[Any]:
        """Get link to a tag"""
        return ["https://neovim.io/doc/user/" + f"{file_name}#{tag}" for file_name, tag in list_of_tags]
