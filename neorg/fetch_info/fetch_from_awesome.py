#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# File Name: fetch_from_awesome.py

import functools
import re
import weakref
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from rapidfuzz import fuzz, process


def fuzzy_dict_search(data_set: dict, fuzz_list: dict, des: str = "desc", search_item: int = 0) -> dict:
    """fuzzy dictionary search, on item given first match

            parameters
            ----------
            item : dict
                item is search value to fuzzy search and filter from both name and dictionary search items
            fuzz_list : dict
                fuzz_list is the filtered list between the name and descroption that are searched through this function
                allows us to filter the matching items and get a valid match
            search_item : int
                search item is a integer value to distringuish between desc[desc] search which searchs descroptions and
                1 where it searches the name of the item

            returns
            -------
            dict
                returns filtered dictionary
            """
    return {
        name: desc[des]
        for name, desc, in data_set.items()
        for i in range(len(fuzz_list))
        if fuzz_list[i][0] == (name if search_item == 1 else desc[des]) and fuzz_list[i][1] > 80
    }


def weak_lru(maxsize: int = 128, typed: bool = False) -> callable:
    """A weakref.WeakKeyDictionary with a limited size.
    If maxsize is 0, the cache has no limit.
    It also is a wrapper due to the fact that the cache is weak.
    """

    def wrapper(func: callable) -> callable:
        """The wrapper function."""

        @functools.lru_cache(maxsize, typed)
        def _func(_self: callable, *args, **kwargs) -> callable:
            """funct that is being wrapped"""
            return func(_self(), *args, **kwargs)

        @functools.wraps(func)
        def inner(self: callable, *args, **kwargs) -> callable:
            """inner function that is called by the wrapper"""
            return _func(weakref.ref(self), *args, **kwargs)

        return inner

    return wrapper


class ReadAwesome:
    """Read Awesome neovim github page to retrieve all the plugins"""

    def __init__(self,) -> None:
        self.soup = BeautifulSoup(
            requests.get("https://raw.githubusercontent.com/rockerBOO/awesome-neovim/main/README.md").text,
            "html.parser",
        )

    @weak_lru(maxsize=None)
    def get_from_header(self) -> dict:
        """Get all links from Awesome neovim

        Returns
        -------
        dict
            return a dictionary of {name: {'link': link, 'desc': description}}
        """
        names = defaultdict(dict)
        pattern = re.compile(r"- \[(.*?)\]\((.*?)\)\s*(.*?)(\.|!)", re.DOTALL | re.MULTILINE)
        # regex matching for [user/repo](link) description .
        name_url = pattern.findall(self.soup.text)
        for j in name_url:
            name = j[0]
            # check if name contains /
            if "/" in name:
                names[name] = {
                    "link": j[1],
                    "desc": j[2]
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
        fuzzy_list = process.extract(item, dict_set.keys(), scorer=fuzz.token_set_ratio, limit=len(dict_set))

        fuuzzy_dict_search = process.extract(
            item, ({name: desc["desc"]
                    for name, desc in dict_set.items()}).values(),
            scorer=fuzz.token_set_ratio,
            limit=len(dict_set),
        )

        # __import__('pdb').set_trace()

        # reduce return repeating code
        return {
            **fuzzy_dict_search(dict_set, fuzzy_list, "desc", 1),
            **fuzzy_dict_search(dict_set, fuuzzy_dict_search, "desc"),
        }

    def get_most_recent_plugin(self) -> list:
        """Get most recent plugin from the merge table

        Returns
        -------
        list
            List of the most recent added plugins, based on  first page of the closed pr page.
        """
        recent_soup = BeautifulSoup(
            requests.get(
                "https://github.com/rockerBOO/awesome-neovim/pulls?q=is%3Apr+sort%3Aupdated-desc+is%3Aclosed").text,
            "html.parser",
        )

        recent_issues = recent_soup.find_all("div", class_="Box-row")
        regex_pattern = re.compile(r"<a aria-label=\"Link to Issue. Add `(.*?)`")
        return [re.findall(regex_pattern, str(i))[0] for i in recent_issues if re.findall(regex_pattern, str(i))]
