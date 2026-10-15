import os
import sys

import cli
import storage


def main():
    if os.path.exists(cli.DATA_FILE):
        try:
            storage.load_requests(cli.DATA_FILE)
            print(f"Loaded existing data from {cli.DATA_FILE}.")
        except ValueError as error:
            print(f"Error: {error}")
            print(f"Fix or move {cli.DATA_FILE} and try again. Nothing was changed.")
            sys.exit(1)
    cli.run_menu()


if __name__ == "__main__":
    main()