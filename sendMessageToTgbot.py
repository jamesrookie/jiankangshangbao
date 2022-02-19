import requests
#rj的专属机器人
TG_TOKEN = "2106557388:AAFoa76sfxWUHrshRH880r12jokRJyPuF_o"
CHAT_ID = '816551561'


def post_tg(message):
    telegram_message = f"{message}"
    params = {
        'chat_id': CHAT_ID,
        'text': telegram_message,
        'parse_mode': 'Markdown',
        'disable_web_page_preview': 'yes',
    }
    telegram_url = 'https://api.telegram.org/bot' + TG_TOKEN + '/sendMessage'
    telegram_req = requests.post(telegram_url, params=params)
    telegram_status = telegram_req.status_code
    print(telegram_req.text)
    if telegram_status == 200:
        print("Info:Telegram Message sent")
    else:
        print("Telegram Error")
