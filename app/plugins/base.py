from abc import ABC, abstractmethod
from linebot.v3.messaging import TextMessage

class BasePlugin(ABC):
    @property
    @abstractmethod
    def command(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def execute(self, text: str, user_id: str) -> TextMessage:
        pass
