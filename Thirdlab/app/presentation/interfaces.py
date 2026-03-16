from abc import ABC, abstractmethod

class IPresentation(ABC):
    """Presentation layer interface placeholder (not used in web UI)."""

    @abstractmethod
    def show_menu(self):
        pass

    @abstractmethod
    def display_message(self, message: str):
        pass
