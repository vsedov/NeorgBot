# Guidelines
This is the core bot for the neorg server, and hence contains the golden rules for contribution

# Golden rule
  - Good commit messages
  - Pep8 Code style
  - Linting and Pre-commit
      - Flake8 and precommit are used to ensure good code
      - Precommit is a powerful tool that helps you automatically lint before you commit, if the linter complains that
      then this would be aborted i.e fixes are required.
      ```
      poetry run task lint
      poetry run task precommit
      ```
      - Yapf, yet another python formatter, is a great tool to format the code base
  - Type Hinting:
  - Logging, use this instead  of print statements
