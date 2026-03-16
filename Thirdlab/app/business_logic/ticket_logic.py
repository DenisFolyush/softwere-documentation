from typing import List, Optional

from app.business_logic.interfaces import IBusinessLogic
from app.data_access.interfaces import IDataAccess
from app.models import Ticket


class TicketBusinessLogic(IBusinessLogic):
    def __init__(self, data_access: IDataAccess):
        # dependency injection of data access layer via interface
        self._data_access = data_access

    def process_file(self, file_path: str) -> None:
        rows = self._data_access.read_csv(file_path)
        tickets: List[Ticket] = []

        for row in rows:
            t = Ticket(
                title=row.get("title", ""),
                description=row.get("description", ""),
                status=row.get("status", "") or "new",
            )
            tickets.append(t)

        self._data_access.save_tickets(tickets)

    def get_all(self) -> List[Ticket]:
        session = self._data_access.session()
        return session.query(Ticket).all()

    def get_by_id(self, tid: int) -> Optional[Ticket]:
        session = self._data_access.session()
        return session.get(Ticket, tid)

    def add(self, data: dict) -> Ticket:
        t = Ticket(**data)
        self._data_access.save_tickets([t])
        return t

    def update(self, tid: int, data: dict) -> None:
        session = self._data_access.session()
        ticket = session.get(Ticket, tid)
        for key, value in data.items():
            setattr(ticket, key, value)
        session.commit()

    def delete(self, tid: int) -> None:
        session = self._data_access.session()
        ticket = session.get(Ticket, tid)
        session.delete(ticket)
        session.commit()
