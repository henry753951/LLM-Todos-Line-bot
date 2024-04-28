from flask import Flask
from api.linebot import route as linebot_route
from api.todo import route as todo_route
import dotenv
import os


# 如果當前目錄有 .env 檔案，則優先使用 .env 檔案中的環境變數
if ".env" in os.listdir():
    dotenv.load_dotenv()

# 創建 Flask 伺服器
# __name__ 代表目前執行的模組
# 如果以主程式執行，__name__ 會是 __main__
# 如果是被引用，__name__ 會是模組名稱（也就是檔案名稱）
app = Flask(__name__)
# 註冊其他模組的路由
# 註冊後，chat.py, keyword.py, echo.py 中的路由就會生效
# 例如 chat.py 中的 /... 就會對應到網址 /chat/... (因為註冊時指定了 url_prefix='/chat')
app.register_blueprint(linebot_route, url_prefix='/linebot')
app.register_blueprint(todo_route, url_prefix='/todo')


@app.route("/")
def isAlive():
    return "OK"


# 主程式進入點
if __name__ == "__main__":
    # 啟動網路伺服器
    app.run(debug=True, port=os.environ.get('port', 5000))
