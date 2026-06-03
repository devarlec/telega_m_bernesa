from flask import Flask, request, redirect
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_USERNAME = "MarkBernesBot"
WEB_APP_URL = "https://devarlec.github.io/telega_m_bernesa/soviet_filv/"

app = Flask(__name__)

@app.route("/gallery")
def gallery():
    return redirect(WEB_APP_URL)

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        
        is_command = (
            text == "/sovietfilmhistory" or 
            text == f"/sovietfilmhistory@{BOT_USERNAME}"
        )
        
        if is_command:
            # Используем HTML-ссылку вместо Markdown — она стабильнее работает на всех платформах
            reply_text = f'🎞️ Диафильм "Советское киноискусство 20-х годов"\n\n👉 <a href="{WEB_APP_URL}">Открыть галерею</a>'
            
            requests.post(f"{TELEGRAM_API}/sendMessage", json={
                "chat_id": chat_id,
                "text": reply_text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            })
    
    return "ok", 200

@app.route("/")
def index():
    return "Bot is running"
