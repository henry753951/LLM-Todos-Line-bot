# line-bot-python-example

## 關於本專案

這裡有幾個使用 line-bot-sdk-python 開發的範例機器人。

## 在 Vercel 上部署

[![使用 Vercel 部署]()](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fgdscnuk%2Fline-bot-python-2023%2Ftree%2Fvercel&env=access_token,channel_secret,google_generativeai_token)

## 在本地端使用

### Python 套件需求

```md
- Python >= 3.8
- Flask==3.0.0
- line_bot_sdk==3.5.0
- python-dotenv==1.0.0
- google-generativeai==0.3.1
```

### 安裝

1. 安裝所需套件

```sh
pip install -r requirements.txt
```

2. 複製 .env.example 並重新命名為 .env
3. 修改 .env 中的內容為你申請到的資訊
4. 執行程式

```sh
python index.py
```

### Webhook URL 路由

| 路由        | 說明             |
| ----------- | ---------------- |
| `/echo/`    | Echo 機器人      |
| `/chat/`    | 生成式 AI 機器人 |
| `/keyword/` | 關鍵字機器人     |

## 授權

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
