# line-bot-python-example

## About The Project

Here are some examples of line bot.

## Usage for Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fgdscnuk%2Fline-bot-python-2023%2Ftree%2Fvercel&env=access_token,channel_secret,google_generativeai_token)


## Usage for local

### Requirements
```md
- Python >= 3.8
- Flask==3.0.0
- line_bot_sdk==3.5.0
- python-dotenv==1.0.0
- google-generativeai==0.3.1
```
### Installation

1. Install requirements

```sh
pip install -r requirements.txt
```

2. Copy `.env.example` and rename to `.env`
3. Change the content in `.env` to your own information
4. Run the program

```sh
python index.py
```

### Webhook URL route
| Route | Description |
| --- | --- |
| `/echo/` | Echo bot |
| `/chat/` | Generative AI bot |
| `/keyword/` | Keyword bot |


## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
