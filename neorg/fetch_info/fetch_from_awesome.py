#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: fetch_from_awesome.py

import functools
import re
import weakref
from collections import defaultdict

import pyinspect as pi
import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz, process


def weak_lru(maxsize=128, typed=False):

    def wrapper(func):

        @functools.lru_cache(maxsize, typed)
        def _func(_self, *args, **kwargs):
            return func(_self(), *args, **kwargs)

        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            return _func(weakref.ref(self), *args, **kwargs)

        return inner

    return wrapper

class ReadAwesome:

    def __init__(self, url: str) -> None:
        self.soup = BeautifulSoup(requests.get(url).text, 'html.parser')

    @weak_lru(maxsize=None)
    def get_from_header(self) -> dict:
        """Get all links from Awesome neovim

        Returns
        -------
        dict
            return a dictionary of {name: {'link': link, 'desc': description}}
        """
        names = defaultdict(dict)
        pattern = re.compile(r"- \[(.*?)\]\((.*?)\)\s*(.*?)\.", re.DOTALL | re.MULTILINE)
        # regex matching for [user/repo](link) description .
        name_url = pattern.findall(self.soup.text)
        for j in name_url:
            name = j[0]
            # check if name contains /
            if '/' in name:
                names[name] = {
                    'link': j[1],
                    'desc': j[2]
                }
            continue
        return names

    def fuzzy(self, item: str = "Kanagawa") -> dict:
        """Fuzzy search on item, return a list of matches

        Parameters
        ----------
        item : str
            Something to search from Awesome neovim that is valid

        Returns
        -------
        dict
            return a dictionary of {name: {'link': link, 'desc': description}}
        """
        dict_set = self.get_from_header()
        fuzzy_list = process.extract(
            item, dict_set.keys(), scorer=fuzz.token_set_ratio, limit=len(dict_set))

        fuuzzy_dict_search = process.extract(
            item, ({name: desc['desc']
                    for name, desc in dict_set.items()}).values(),
            scorer=fuzz.token_set_ratio,
            limit=len(dict_set))

        # __import__('pdb').set_trace()

        # reduce return repeating code
        def _fuzzy_dict_search(item: dict, fuzz_list: dict, search_item: int = 0) -> dict:
            """Fuzzy dictionary search, on item given first match

            Parameters
            ----------
            item : dict
                item is search value to fuzzy search and filter from both name and dictionary search items
            fuzz_list : dict
                fuzz_list is the filtered list between the name and descroption that are searched through this function
                allows us to filter the matching items and get a valid match
            search_item : int
                search item is a integer value to distringuish between desc[desc] search which searchs descroptions and
                1 where it searches the name of the item

            Returns
            -------
            dict
                returns filtered dictionary
            """
            return {
                name: desc['desc']
                for name, desc, in dict_set.items()
                for i in range(len(fuzz_list))
                if fuzz_list[i][0] == (
                    name if search_item == 1 else desc['desc']) and fuzz_list[i][1] > 80
            }

        return {
            **_fuzzy_dict_search(item, fuzzy_list, 1),
            **_fuzzy_dict_search(item, fuuzzy_dict_search)
        }

def main() -> None:
    url = "https://raw.githubusercontent.com/rockerBOO/awesome-neovim/main/README.md"
    read_awesome = ReadAwesome(url)

    # ic(read_awesome.fuzzy(input("Search: ")))

if __name__ == "__main__":
    pi.install_traceback(enable_prompt=True)
    main()
