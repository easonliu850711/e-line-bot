from linebot.v3.messaging import TextMessage
from .base import BasePlugin

class HelpPlugin(BasePlugin):
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    @property
    def command(self) -> str:
        return "help"

    @property
    def description(self) -> str:
        return "顯示可用指令清單"

    def execute(self, text: str, user_id: str) -> TextMessage:
        lines = ["🌸 Moltbot 可用指令："]
        for cmd, plugin in self.dispatcher.plugins.items():
            lines.append(f"- {cmd}: {plugin.description}")
        return TextMessage(text="\n".join(lines))
