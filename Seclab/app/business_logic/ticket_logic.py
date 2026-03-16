from typing import List

from app.business_logic.interfaces import IBusinessLogic
from app.data_access.interfaces import IDataAccess
from app.models import Ticket


class TicketBusinessLogic(IBusinessLogic):
    def __init__(self, data_access: IDataAccess):
        # dependency injection of data access layer via interface
        self._data_access = data_access

    def process_file(self, file_path: str) -> None:
        # read raw rows from CSV
        rows = self._data_access.read_csv(file_path)
        tickets: List[Ticket] = []

        for row in rows:
            # basic conversion logic; expecting headers: title,description,status
            t = Ticket(
                title=row.get("title", ""),
                description=row.get("description", ""),
                status=row.get("status", "") or "new",
            )
            tickets.append(t)

        # persist to database
        self._data_access.save_tickets(tickets)
