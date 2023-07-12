import json

import requests
from icecream import ic
from rapidfuzz import fuzz, process

from neorg import constants
from neorg.fetch_info.fetch_from_awesome import fuzzy_dict_search
from neorg.log import get_logger

log = get_logger(__name__)


class FetchDatabase(object):
    """Fetch information from the pnp database, and return a dictionary of information."""

    def __init__(self):
        log.info(ic.format("Init being used thing woosh"))
        self.database_link = "https://raw.githubusercontent.com/nvim-plugnplay/database/main/database.json"
        self.database = {}

        self.filtered_values: list["str"] = [
            "clone_url",
            "created_at",
            "default_branch",
            "description",
            "language",
            "full_name",
            "open_issues_count",
            "updated_at",
        ]
        self.fetch_database()
        self.write_to_file()

    def fetch_database(self) -> None:
        """Fetch database from github."""
        log.info("Fetching database")
        with requests.Session() as session:
            response = session.get(self.database_link)
            # load directly to items()
            loaded_data = json.loads(response.text).items()
            for key, value in loaded_data:
                self.database[key] = {
                    k: v for k, v in value.items() if k in self.filtered_values
                }

    def write_to_file(self) -> None:
        log.info("Writing to file")
        with open(constants.PNP_DATABAS_FILE, "w") as f:
            f.write(json.dumps(self.database, sort_keys=True, indent=4))

    def open_database(self) -> None:
        """open the database.json file and return the database."""
        with open(constants.PNP_DATABAS_FILE) as f:
            database = json.load(f)
        return database

    def search_fuzzy(self, search_item: str = "neorg") -> list[dict]:
        """
        fuzzy search item from the database, this will not search description, but if you refer to
        search_awesome folder, and fetch_info.Abstracted functions can be used to also search
        description or any other attributes of the database.
        """
        log.info(ic.format(f"Searching for {search_item}"))

        database = self.open_database()

        fuzzy_name_search = process.extract(
            search_item,
            database.keys(),
            scorer=fuzz.token_set_ratio,
            limit=len(database),
        )

        fuzzy_description_search = process.extract(
            search_item,
            (
                {name: desc["description"] for name, desc in database.items()}
            ).values(),
            scorer=fuzz.token_set_ratio,
            limit=len(database),
        )

        # refer to neorg.ext.fetch_info.fetch_from_awesome.fuzzy_dict_search
        data = {
            **fuzzy_dict_search(database, fuzzy_name_search, "description", 1),
            **fuzzy_dict_search(
                database, fuzzy_description_search, "description"
            ),
        }
        return [database[v] for v in data]
