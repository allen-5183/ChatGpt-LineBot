from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT
import os
line_bot_api = LineBotApi(os.getenv("/N21PSTAF9y/VMdKstv4IhOfLRuQStz06mENh56qRA70t5jkMej7dTnaPV6TaM/hUmwjOMwDYO5JP8GFP3T1n9XhsluprO3OdecNN0FGbMURQYMSqYgPBSWHe3U0cuoNA+Qveq6XU+SGY8GQ93op+QdB04t89/1O/w1cDnyilFU="))
line_handler = WebhookHandler(os.getenv("ed2b9ae51fb839bb388f04b98557d357"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"
app = Flask(__name__)
chatgpt = ChatGPT()
# domain root
@app.route('/')
def home():
    return 'Hello, World!'
@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    
    if event.message.type != "text":
        return
    working_status = True
    if working_status:
        chatgpt.add_msg(f"Human:{event.message.text}?\n")
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        chatgpt.add_msg(f"AI:{reply_msg}\n")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))
if __name__ == "__main__":
    app.run()