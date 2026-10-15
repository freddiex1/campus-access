import storage
import workflow

DATA_FILE = "data.json"

MENU = """
=== Campus Access Card Manager ===
1. Create request
2. View request
3. Approve request
4. Issue card
5. Return card
6. List requests
7. Save
8. Load
9. Quit"""


def format_request(r):
    return (f"{r['id']} | fellow: {r['fellow_id']} | type: {r['card_type']} "
            f"| status: {r['status']} | approved_by: {r['approved_by']}")


def run_menu(input_func=input, output_func=print, data_file=DATA_FILE):
    while True:
        output_func(MENU)
        try:
            choice = input_func("Choose: ").strip()
        except EOFError:
            output_func("Input ended. Exiting.")
            return

        try:
            if choice == "1":
                fellow_id = input_func("Fellow ID: ")
                card_type = input_func("Card type (visitor/student/staff): ").strip().lower()
                record = storage.create_request(fellow_id, card_type)
                output_func(f"Created {format_request(record)}")
            elif choice == "2":
                record = storage.get_request(input_func("Request ID: ").strip())
                output_func(format_request(record))
            elif choice == "3":
                request_id = input_func("Request ID: ").strip()
                approver = input_func("Approved by: ")
                workflow.approve_request(request_id, approver)
                output_func(f"{request_id} is now approved.")
            elif choice == "4":
                request_id = input_func("Request ID: ").strip()
                workflow.issue_card(request_id)
                output_func(f"{request_id} is now issued.")
            elif choice == "5":
                request_id = input_func("Request ID: ").strip()
                workflow.return_card(request_id)
                output_func(f"{request_id} is now returned.")
            elif choice == "6":
                records = storage.list_requests()
                if not records:
                    output_func("No requests yet.")
                for record in records:
                    output_func(format_request(record))
            elif choice == "7":
                storage.save_requests(data_file)
                output_func(f"Saved to {data_file}.")
            elif choice == "8":
                storage.load_requests(data_file)
                output_func(f"Loaded from {data_file}.")
            elif choice == "9":
                answer = input_func("Save before quitting? (y/n): ").strip().lower()
                if answer == "y":
                    storage.save_requests(data_file)
                    output_func(f"Saved to {data_file}.")
                output_func("Goodbye.")
                return
            else:
                output_func(f"Invalid option '{choice}'. Please choose 1-9.")
        except ValueError as error:
            output_func(f"Error: {error}")