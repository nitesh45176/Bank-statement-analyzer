from abc import ABC, abstractmethod


class BaseParser(ABC):

    @abstractmethod
    def parse_transactions(self, rows):
        """Convert grouped rows into Transaction objects."""
        pass

    @abstractmethod
    def parse_account_details(self, text):
        """Extract account metadata."""
        pass