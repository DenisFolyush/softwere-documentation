"""Keep this module simple: wire dependencies and run business logic from the command line."""
import sys
from pathlib import Path

from app.business_logic.ticket_logic import TicketBusinessLogic
from app.data_access.sql_data_access import SQLDataAccess


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m app.main <data.csv>")
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        print(f"File {csv_path} does not exist.")
        sys.exit(1)

    # instantiate data access via interface
    data_access = SQLDataAccess()
    logic = TicketBusinessLogic(data_access)
    logic.process_file(str(csv_path))
    print("Processing complete.")


if __name__ == "__main__":
    main()
