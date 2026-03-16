from abc import ABC, abstractmethod

class IPresentation(ABC):
    """Presentation layer interfaces - currently no logic implemented."""

    @abstractmethod
    def show_menu(self):
        pass

    @abstractmethod
    def display_message(self, message: str):
        pass
