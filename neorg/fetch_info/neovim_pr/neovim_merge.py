#!/usr/bin/python3

import json

import requests

from neorg.log import get_logger

log = get_logger(__name__)


def get_open_pullrequests() -> str:
    """Temp documentation."""
    url = "https://api.github.com/repos/neovim/neovim/pulls?state=open&per_page=100"
    r = requests.get(url)
    r.raise_for_status()

    def get_pr_number(pr: str) -> str:
        """Get pr number"""

        return pr.split("/")[-1]

    data = r.json()
    with open("test_file.json", "w") as r:
        json.dump(data, r, indent=4, sort_keys=True)

    # prs = sorted(
    #     (
    #         {"pr_number": get_pr_number(
    #             pull["html_url"]), "html_url": pull["html_url"], "title": pull["title"]}
    #         for pull in r.json()
    #     ),
    #     key=lambda x: get_pr_number(x["html_url"]),
    # )


if __name__ == "__main__":
    pull_requests = get_open_pullrequests()
    log.info(pull_requests)
