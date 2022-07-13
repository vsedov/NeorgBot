import asyncio
import functools
import itertools as it

import requests
from icecream import ic

from neorg import constants
from neorg.fetch_info.neovim_pr.model import PRRequestModel
from neorg.log import get_logger

# from joblib import Parallel, delayed

log = get_logger(__name__)


def get_or_create_eventloop() -> asyncio:
    """
    Gets the current asyncio event loop, and only creats one within the main thread.

    Returns
    -------
    asyncio
        The current created asycnio event loop
    """
    try:
        return asyncio.get_event_loop()
    except RuntimeError as error:
        if "There is no current event loop in thread" in (er := (str(error))):
            log.info(f"Creating an event loop based on {er}")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


class Test:
    """Temp documentation."""

    def __init__(self, user: str = "neovim"):
        self.user = user
        self.user_fmt = ic.format(self.user)
        self.base_url = f"https://api.github.com/repos/neovim/{self.user}/pulls?state=open&per_page="
        self.client_id = constants.CLIENT_ID
        self.client_secret = constants.CLIENT_SECRET
        self.batch_size = 10

        # if not self.client_id() or not self.client_secret():
        #     log.info("Client id or client secret is None, api will fail.")
        #     return

    def load_pr_results(self, page: int) -> PRRequestModel:
        """Load pr results / requests through batches of 10: this is a request to the page it self

        Parameters
        ----------
        page : int
            page number to take requestion from :
            example : https://api.github.com/repos/neovim/neovim/pulls?state=open&per_page=100

        Returns
        -------
        PRRequestModel
            Pydantic Base model
        """
        log.debug(f"Querying for pull request {self.user_fmt}, {page}")
        response = requests.get(self.base_url + str(page), auth=(self.client_id, self.client_secret))
        response.raise_for_status()
        if response.status_code == 200:
            output_response = PRRequestModel(response=response.json())
            if len(output_response.response) == 0:
                log.info(f"No pages were found {self.user_fmt}, {page}")

        return output_response

    async def get_pages(self) -> PRRequestModel:
        """
        get all pages from neovim source pr, this will grab, 10 pages at a time, till no pages are found.
        Returns
        -------
        response : PRRequestModel
        """
        loop = get_or_create_eventloop()
        results = []
        finished = False
        start = 0
        batch_size = self.batch_size
        while not finished:
            temp = await asyncio.gather(
                *[
                    loop.run_in_executor(
                        None,
                        functools.partial(self.load_pr_results, start + i),
                    ) for i in range(1, batch_size + 1)
                ])

            temp = PRRequestModel(response=list(it.chain(*[value.response for value in temp])))
            log.info(len(temp.response))

            if len(temp.response) == 1000:
                log.info("temp response == 0 Finish batch result")
                finished = True
            results += temp.response
            start += batch_size
        return PRRequestModel(response=results)

    def make_jobs(self, base: PRRequestModel) -> None:
        """
        Make Jobs : given response list, generate jobs, this will allow us to extract_data at the same time
        This function will iterate through the response list, and for each given response, creates file container
        recent prs: Edge cases can be modular

        Parameters
        ----------
        base : PRRequestModel
            PRRequestModel : Pydantic Model
        """
        log.info(base)
        breakpoint()

        # creation_jobs= Parallel(-1)(delayed())

    def __call__(self):
        """Temp documentation."""
        loop = get_or_create_eventloop()  # noqa: ignore
        log.info(f"Creting event loop for {self.user_fmt}")
        base = asyncio.run(self.get_pages())
        self.make_jobs(base)


if __name__ == "__main__":
    test = Test()
    test_2 = test()
