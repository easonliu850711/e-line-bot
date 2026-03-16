from datetime import datetime
from linebot.v3.messaging import TextMessage
from .base import BasePlugin

class PingPlugin(BasePlugin):
    @property
    def command(self) -> str:
        return "ping"

    @property
    def description(self) -> str:
        return "檢查系統狀態與當前時間"

    def execute(self, text: str, user_id: str) -> TextMessage:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = (
            "🌸 Moltbot LINE adapter OK\n"
            f"📍 Time (JST): {now}\n"
            "⚡ Status: Online & Ready"
        )
        return TextMessage(text=msg)
