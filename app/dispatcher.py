from linebot.v3.messaging import TextMessage
from app.plugins.ping import PingPlugin
from app.plugins.help import HelpPlugin

class CommandDispatcher:
    def __init__(self):
        self.plugins = {}
        self._register_plugins()

    def _register_plugins(self):
        ping_plugin = PingPlugin()
        self.plugins[ping_plugin.command] = ping_plugin
        help_plugin = HelpPlugin(self)
        self.plugins[help_plugin.command] = help_plugin

    def dispatch(self, text: str, user_id: str) -> TextMessage:
        text = text.strip()
        if not text:
            return TextMessage(text="請輸入指令，或輸入 help 查看清單。")
        command = text.split()[0].lower()
        plugin = self.plugins.get(command)
        if plugin:
            try:
                return plugin.execute(text, user_id)
            except Exception as e:
                return TextMessage(text=f"執行 {command} 時發生錯誤。")
        return TextMessage(text=f"未知指令：{command}。請輸入 help 查看清單。")

dispatcher = CommandDispatcher()
