from abc import ABC, abstractmethod
from typing import List, Dict

class IDataAccess(ABC):
    """Interface for the data access layer. Business logic should depend on this, not concrete implementations."""

    @abstractmethod
    def read_csv(self, file_path: str) -> List[Dict[str, str]]:
        """Read rows from a CSV file.
        Returns a list of dictionaries mapping column names to values.
        """
        pass

    @abstractmethod
    def save_tickets(self, tickets: List[object]) -> None:
        """Persist a list of ticket-like objects into the database."""
        pass

    @abstractmethod
    def get_all_tickets(self) -> List[object]:
        """Return all persisted tickets from the database."""
        pass
