# reference : https://github.com/heraldofsolace/VimHelpBot
import os
import re
import sqlite3

from neorg import constants
from neorg.fetch_info.get_documentation import doc_setup
from neorg.log import get_logger

log = get_logger(__name__)

tag_re = re.compile(r'^(\S+)\s*(\S+).txt', re.MULTILINE)


def add_tags(software: str, c: sqlite3.Connection) -> None:
    """Add tags to the tag database"""
    if not os.path.exists(constants.THIRD_PARTY_PATH + 'neovim'):
        doc_setup()

    with open(constants.THIRD_PARTY_PATH + software + '/runtime/doc/tags') as f:
        text = f.read()
        matches = tag_re.findall(text)

        for m in matches:
            # db entry: (doc, tag, software)
            entry = (m[1], m[0])
            c.execute('INSERT OR REPLACE INTO tags VALUES (?,?)', entry)
            log.info(f'{software}/{m[1]} => {m[0]}')


def tag_setup() -> None:
    """Setup the tag database"""
    conn = sqlite3.connect(constants.DATABASE_PATH + '/tags.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tags(filename text, tag text)")
    add_tags("neovim", c)
    conn.commit()
    conn.close()
    os.system('rm -rf ' + constants.THIRD_PARTY_PATH)


def inital_tag_setup() -> None:
    """Initial setup for the tag database"""
    doc_setup()
    tag_setup()
