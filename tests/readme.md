# Testing the bot
With respect to this bot I hope that this will have a large test coverage through the code base. Fundamentally I do not want things to break when hosting,  and it is best practice to have test cases for this.
Such that I understand that discord is a rather hard thing to test properly, and that is fine. The goal for this is to have a minimum test coverage of 70 % for both documentation and test suits.

_Note_ This is more a guide of how to test bots but not on how to write unit tests

## Tools

Main tools are the following

### Unit test
- [UnitTest](https://docs.python.org/3/library/unittest.html)
- [Unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Coverage.py](https://coverage.readthedocs.io/en/stable/)
- [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/index.html)

### Test
- [TestRunner pytest](pytest-cov)

### Documentation standard
- [PDOC](https://pdoc.dev/)
- [Interrogate](https://github.com/econchick/interrogate)

## How to test
Poetry offers a broad ways of testing a given project, you can use _tox_ or poetry it self to build a package / test it
To ensure that the results you obtain are personal to your machine, its important to have the following things setup

[Poetry Project Env](https://github.com/python-discord/bot/blob/main/pyproject.toml) this will allow you to run test cases with poetry with given short cuts provided with the following commands

### Tests
poetry run task test-nocov
will run pytest

poetry run task test
Will run _Pytest_ with _pytest-cov_

poetry run task test tests/folder/test.py
Will run a specific test

poetry run task report
Will generate report and coverage report of the test you have run with

**Important note** If you want the coverage report first then you would have to ensure that you run
poetry run task test
### Documentation
Run
```
poetry run task doc
```
This will run an Interrogate report, which will ensure the code base that we have is well documented

### Command List
```
start = "python -m neorg"
lint = "pre-commit run --all-files"
precommit = "pre-commit install"
test-nocov = "pytest -n auto"
test = "pytest -n auto --cov-report= --cov --ff"
retest = "pytest -n auto --cov-report= --cov --lf"
html = "coverage html"
report = "coverage report"
doc = "interrogate -c pyproject.toml"
isort = "isort ."
```
running the following
_poetry run task (start, lint, precommit, test-nocov, test, retest, html, report, doc, isort)_
are full list of valid commands you can use

# Dev Notes
Poetry offers allot, For active development you can do the following to make your life easier
1. Set up poetry
2. Create an env using _poetry env use python_
3. Install Direnv and inside the repo create an .envrc
4. Run the following
```
nvim $HOME/.direnvrc
```

Once inside
```
  layout_poetry() {
  if [[ ! -f pyproject.toml ]]; then
      log_error 'No pyproject.toml found. Use `poetry new` or `poetry init` to create one first.'
      exit 2
  fi

  local VENV=$(poetry env list --full-path | cut -d' ' -f1)
  if [[ -z $VENV || ! -d $VENV/bin ]]; then
      log_error 'No poetry virtual environment found. Use `poetry install` to create one first.'
      exit 2
  fi

  export VIRTUAL_ENV=$VENV
  export POETRY_ACTIVE=1
  PATH_add "$VENV/bin"
  }
```

Now in your _.envrc_ we can put _layout_poetry_ and this will auto env into your directory for you
