import os

from neorg import constants
from neorg.log import get_logger

log = get_logger(__name__)


def doc_setup() -> None:
    """Get documentation from neovim"""
    if not os.path.exists(f'{constants.THIRD_PARTY_PATH}/neovim'):
        # cd to fet_nifo foldder
        os.chdir(constants.FETCH_INFO_PATH)
        os.system('git clone --branch nightly https://github.com/neovim/neovim.git third_party/neovim')
    else:
        os.system(f'git -C {constants.THIRD_PARTY_PATH}/neovim pull')

    os.system(
        f'vim --clean -e --cmd "helptags{constants.THIRD_PARTY_PATH}/neovim/runtime/doc | quit"'
    )
    if not os.path.exists(constants.DATABASE_PATH):
        os.mkdir(constants.DATABASE_PATH)
