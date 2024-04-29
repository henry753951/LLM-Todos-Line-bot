# 引入需要的模組
from collections import defaultdict
from flask import request, abort, Blueprint, current_app
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import dotenv
import os
import requests
import datetime
import time

# 如果當前目錄有 .env 檔案，則優先使用 .env 檔案中的環境變數
if ".env" in os.listdir():
    dotenv.load_dotenv()


class Dify:
    lastCompletion = datetime.datetime.now()

    def __init__(self):
        api_key = os.environ.get("dify_api_key", "")
        self.api = os.environ.get("dify_api", "")
        self.headers = {"Authorization": F"Bearer {api_key}", "Content-Type": "application/json"}

    def chat(self, user_id: str, text: str, conversation_id: str = None):
        # Microsoft Azure API 預設限制
        while (datetime.datetime.now() - self.lastCompletion).total_seconds() < 10:
            time.sleep(1)

        url = F"{self.api}/v1/chat-messages"
        data = {"inputs": {}, "query": text, "user": user_id, "response_mode": "blocking"}
        if conversation_id:
            data["conversation_id"] = conversation_id
        self.lastCompletion = datetime.datetime.now()
        response = requests.post(url, headers=self.headers, json=data)
        return {
            "conversation_id": str(response.json().get("conversation_id")),
            "reply": str(response.json().get("answer")),
        }


dify = Dify()

_access_token = os.environ.get("access_token")
_channel_secret = os.environ.get("channel_secret")

# 建立一個新的藍圖
route = Blueprint(name="__linebot", import_name=__name__)

# 設定 Line Bot 的設定
configuration = Configuration(access_token=_access_token)
line_handler = WebhookHandler(_channel_secret)


# 建立一個使用者字典，用於儲存conversation id
users = defaultdict(lambda: {"conversation": None})


# 定義一個路由，用於接收 Line Bot 的訊息
@route.route("/", methods=["POST"])
def chat_callback():
    # 取得 Line Bot 的認證資訊
    signature = request.headers["X-Line-Signature"]

    # 取得請求的內容
    body = request.get_data(as_text=True)
    current_app.logger.info("Request body: " + body)

    # 處理 webhook 的內容
    # 若驗證失敗，則回傳錯誤訊息 (400)
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        current_app.logger.error(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


# 定義一個處理訊息的函數
@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    with ApiClient(configuration) as api_client:
        current_app.logger.debug("User:" + event.source.to_dict()["userId"])
        # 取得使用者的對話
        if "reset" == event.message.text:
            users[event.source.to_dict()["userId"]]["conversation"] = None
            reply = "對話已重置"
        else:
            response = dify.chat(
                user_id=event.source.to_dict()["userId"],
                text=event.message.text,
                conversation_id=users[event.source.to_dict()["userId"]]["conversation"],
            )
            users[event.source.to_dict()["userId"]]["conversation"] = response["conversation_id"]
            reply = response["reply"]
        # 使用 Line Bot API 回覆訊息
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=event.reply_token, messages=[TextMessage(text=reply)])
        )
