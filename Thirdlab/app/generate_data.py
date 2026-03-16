import csv
from pathlib import Path

from app.data_access.sql_data_access import SQLDataAccess
from app.business_logic.ticket_logic import TicketBusinessLogic


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m app.generate_data <data.csv>")
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        print(f"File {csv_path} does not exist.")
        sys.exit(1)

    data_access = SQLDataAccess()
    logic = TicketBusinessLogic(data_access)
    logic.process_file(str(csv_path))
    print("Processing complete.")


if __name__ == "__main__":
    import sys
    main()
