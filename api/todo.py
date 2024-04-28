# 引入需要的模組
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

# 如果當前目錄有 .env 檔案，則優先使用 .env 檔案中的環境變數
if ".env" in os.listdir():
    dotenv.load_dotenv()

# 從環境變數中取得需要的資訊
_access_token = os.environ.get('access_token')
_channel_secret = os.environ.get('channel_secret')

# 建立一個新的藍圖
route = Blueprint(name="__echo", import_name=__name__)

# 設定 Line Bot 的設定
configuration = Configuration(access_token=_access_token)
line_handler = WebhookHandler(_channel_secret)

# 伺服器在收到 POST 請求 /echo 時，會執行 callback 函式處理
@route.route("/", methods=['POST'])
def callback():
    # 獲取 Header 中 X-Line-Signature 的值
    signature = request.headers['X-Line-Signature']

    # 把請求內容取出
    body = request.get_data(as_text=True)
    current_app.logger.info("Request body: " + body)

    # 處理請求
    try:
        # 把 body 跟 signature 交給 handler 做處理
        line_handler.handle(body, signature)
    # 如果有錯誤，把錯誤內容列印出來
    except InvalidSignatureError:
        current_app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 透過 handler_message 函式處理 MessageEvent 中的 TextMessageContent
@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # MessageEvent 中的 TextMessageContent 大概會有下面這些內容
    # {
    #   "type": "message",
    #   "message": {
    #     "type": "text",
    #     "id": "14353798921116",
    #     "text": "Hello, world"
    #   },
    #   "timestamp": 1625665242211,
    #   "source": {
    #     "type": "user",
    #     "userId": "U80696558e1aa831..."
    #   },
    #   "replyToken": "757913772c4646b784d4b7ce46d12671",
    #   "mode": "active",
    #   "webhookEventId": "01FZ74A0TDDPYRVKNK77XKC3ZR",
    #   "deliveryContext": {
    #     "isRedelivery": false
    #   }
    # }
    # 有些內容我們用不到，所以只取出我們需要的（像是 event.message.text 和 event.reply_token）

    # 透過 ApiClient 建立一個 LineBotApi
    with ApiClient(configuration) as api_client:
        # 透過 LineBotApi 建立一個 MessagingApi
        line_bot_api = MessagingApi(api_client)
        # 回覆訊息
        line_bot_api.reply_message_with_http_info(
            # 回覆訊息的 request
            ReplyMessageRequest(
                reply_token=event.reply_token, 
                messages=[TextMessage(text=event.message.text)]
            )
        )