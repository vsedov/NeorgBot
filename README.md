<div align="center">

<img src="img/neorg-bot.png" width=300>

# NeorgBot - A Bot For The Neorg Discord Server

<a href="https://discord.gg/T6EgTAX7ht"> ![Discord](https://img.shields.io/badge/discord-join-7289da?style=for-the-badge&logo=discord) </a>
<a href="https://github.com/nvim-neorg/neorg"> ![GitHub](https://img.shields.io/badge/Neorg%20-visit-blue.svg?style=for-the-badge&logo=GitHub) </a>
<a href="/LICENSE"> ![License](https://img.shields.io/badge/license-GPL%20v3-brightgreen?style=for-the-badge)</a>

[Summary](#summary)
•
[Setup](#setup)
•
[Usage](#usage)
<br>

</div>

<div align="center">

<br>

## Summary

</div>

This is a bot for the Neorg discord server, to be used for searching through the Neorg wiki and spec; many other quality of life features e.g. searching through YouTube videos, pulling up Neovim documentation etc.

## Setup
**Python 3.10 is recommended.**

Start by cloning the repository with `git clone git@github.com:vsedov/NeorgBot.git`.

### Dependencies

1. Install [poetry](https://github.com/python-poetry/poetry) by following the [instructions](https://python-poetry.org/docs/master/#installing-with-the-official-installer).
2. Create an environment with `poetry env use python`.
3. Run `poetry update` to install the dependencies listed in the [pyproject.toml](https://github.com/vsedov/NeorgBot/blob/master/pyproject.toml) file.

## Usage

After installation of the dependencies, run the bot with `poetry run task start`.

**IMPORTANT:** Before making a pull request, test whether your code works as intended and has passed all checks from the linters with `poetry run task test`. For additional information we recommend reading the [readme.md](https://github.com/vsedov/NeorgBot/blob/master/tests/readme.md) file found in the `tests` folder.
