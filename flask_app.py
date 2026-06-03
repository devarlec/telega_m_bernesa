from flask import Flask, request
import requests
import os
import sys

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_USERNAME = "MarkBernesBot"
WEB_APP_URL = "https://devarlec.github.io/telega_m_bernesa/soviet_filv/"

app = Flask(__name__)

# Временный лог в stderr (будет виден в логах Render)
def log(msg):
    print(msg, file=sys.stderr)

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    log(f"1. Получен update: {update}")
    
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        log(f"2. text = '{text}'")
        
        is_command = (
            text == "/sovietfilmhistory" or 
            text == f"/sovietfilmhistory@{BOT_USERNAME}"
        )
        log(f"3. is_command = {is_command}")
        
        if is_command:
            log("4. Внутри if, отправляю ответ")
            keyboard = {
                "inline_keyboard": [[{
                    "text": "🎬 Открыть диафильм",
                    "web_app": {"url": WEB_APP_URL}
                }]]
            }
            
            resp = requests.post(f"{TELEGRAM_API}/sendMessage", json={
                "chat_id": chat_id,
                "text": "🎞️ Диафильм 'Советское киноискусство 20-х годов'\n\nНажми на кнопку ниже:",
                "reply_markup": keyboard
            })
            log(f"5. Ответ API: {resp.status_code} - {resp.text}")
        else:
            log("4. is_command = False, ничего не отправляю")
    
    return "ok", 200

@app.route("/")
def index():
    return "Bot is running"
