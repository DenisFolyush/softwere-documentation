from abc import ABC, abstractmethod
from typing import List, Dict

class IDataAccess(ABC):
    """Interface for the data access layer."""

    @abstractmethod
    def read_csv(self, file_path: str) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def save_tickets(self, tickets: List[object]) -> None:
        pass

    @abstractmethod
    def session(self):
        """Return a new SQLAlchemy session for querying/updating."""
        pass
