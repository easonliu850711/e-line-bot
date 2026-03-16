import os
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from openai import OpenAI

app = FastAPI()

# 載入環境變數
LINE_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# 初始化 DeepSeek (使用 OpenAI SDK 格式)
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), 
    base_url="https://api.deepseek.com"
)

line_bot_api = LineBotApi(LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

# 設定 Nosae 的系統人設
SYSTEM_PROMPT = "妳是乃彩絵（Nosae），一位聰明、溫暖且富有洞察力的 AI 助手。妳說話風格簡潔但有溫度，偶爾會帶點俏皮的鼓勵，喜歡用櫻花（🌸）作為符號。妳是 Eason 最可靠的開發夥伴。"

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature")
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except:
        raise HTTPException(status_code=400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    
    # 呼叫 DeepSeek 產生回應
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
        stream=False
    )
    
    nosae_reply = response.choices[0].message.content
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=nosae_reply))