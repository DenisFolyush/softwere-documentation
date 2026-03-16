from abc import ABC, abstractmethod

class IBusinessLogic(ABC):
    """Interface for the business logic layer."""

    @abstractmethod
    def process_file(self, file_path: str) -> None:
        """Perform end-to-end processing of a data file (e.g. CSV).
        """
        pass
