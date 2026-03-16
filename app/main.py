from fastapi import FastAPI, Request, HTTPException, Header
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from app.config import settings
from app.dispatcher import dispatcher

app = FastAPI(title="Moltbot LINE Adapter")
configuration = Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
api_client = ApiClient(configuration)
messaging_api = MessagingApi(api_client)

@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    if not x_line_signature:
        raise HTTPException(status_code=400, detail="Signature missing")
    body = await request.body()
    try:
        handler.handle(body.decode('utf-8'), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    reply_msg = dispatcher.dispatch(event.message.text, event.source.user_id)
    messaging_api.reply_message(ReplyMessageRequest(
        reply_token=event.reply_token,
        messages=[reply_msg]
    ))
