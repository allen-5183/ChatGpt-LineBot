from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT
import os
line_bot_api = LineBotApi(os.getenv("v1RlGrqSFa/Bu8AEb6JjNkyKpaIIodb0R62NTENyHIVxzVLOmjHPYFSPCpG/qDOKxkcuYr3NQ093XskkDAlG6otmqM2GJ1p7U2lu6keaxf3Z4Q5JOZhtIymJxsyC128KHVEgz2kpVnypiKUt1+ckswdB04t89/1O/w1cDnyilFU="))
line_handler = WebhookHandler(os.getenv("605a0481a6f892fa0e83aff491939cfe"))
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