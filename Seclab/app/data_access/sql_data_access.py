import csv
from typing import List, Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.data_access.interfaces import IDataAccess
from app.models import Ticket, Base


class SQLDataAccess(IDataAccess):
    def __init__(self, db_url: str = "sqlite:///tickets.db"):
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def read_csv(self, file_path: str) -> List[Dict[str, str]]:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]

    def save_tickets(self, tickets: List[Ticket]) -> None:
        session = self.Session()
        try:
            session.add_all(tickets)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_all_tickets(self) -> List[Ticket]:
        session = self.Session()
        try:
            return session.query(Ticket).all()
        finally:
            session.close()
