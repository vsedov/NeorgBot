import requests

from neorg.constants import CLIENT_ID, CLIENT_SECRET
from neorg.log import get_logger

log = get_logger(__name__)

# check if pr is merged


def check_pr_merged(pr_number: int = 19306) -> None:
    """Test playground to check prs have been merged using api"""

    # Check if this Pr is merged using requests
    # repo = 'neovim/neovim'
    repo = 'neovim/neovim'
    url = f'https://api.github.com/repos/{repo}/pulls/{pr_number}'

    response = requests.get(url, auth=(CLIENT_ID, CLIENT_SECRET))

    return response.json()['merged_at']


log.info(check_pr_merged())
