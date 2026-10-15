# campus-access
campus access-card requests, including request creation, approval, card issuing, returns, JSON data persistence, input validation, and automated unit testing.
# Campus Access Card Manager

A Python command-line app to create, approve, issue and return campus access cards.
It uses only the Python standard library.

## Run
python3 main.py

## Test
python3 -m unittest discover -s tests -v

## Workflow
requested -> approved -> issued -> returned (returned is final)

## Files
- storage.py: create, look up, save and load requests
- workflow.py: approve, issue, return
- cli.py: the menu
- main.py: starts the program

