from flask import Flask, request
import requests
import os

# Токен берем из переменных окружения Render
BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_USERNAME = "MarkBernesBot"
WEB_APP_URL = "https://devarlec.github.io/telega_m_bernesa/soviet_filv/"

app = Flask(__name__)

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        
        # Проверяем команду (с @username или без)
        is_command = (
            text == "/sovietfilmhistory" or 
            text == f"/sovietfilmhistory@{BOT_USERNAME}"
        )
        
        if is_command:
            # Создаем кнопку с WebApp
            keyboard = {
                "inline_keyboard": [[{
                    "text": "🎬 Открыть диафильм",
                    "web_app": {"url": WEB_APP_URL}
                }]]
            }
            
            # Отправляем сообщение с кнопкой
            requests.post(f"{TELEGRAM_API}/sendMessage", json={
                "chat_id": chat_id,
                "text": "🎞️ Диафильм 'Советское киноискусство 20-х годов'\n\nНажми на кнопку ниже:",
                "reply_markup": keyboard
            })
    
    return "ok", 200

@app.route("/")
def index():
    return "Bot is running"
