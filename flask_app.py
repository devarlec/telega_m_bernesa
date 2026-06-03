from flask import Flask, request, redirect
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_USERNAME = "MarkBernesBot"
WEB_APP_URL = "https://devarlec.github.io/telega_m_bernesa/soviet_filv/"

app = Flask(__name__)

# Короткий адрес для галереи
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
        chat_type = update["message"]["chat"]["type"]
        
        is_command = (
            text == "/sovietfilmhistory" or 
            text == f"/sovietfilmhistory@{BOT_USERNAME}"
        )
        
        if is_command:
            # Короткая ссылка вместо длинной
            short_url = "https://telega-m-bernesa.onrender.com/gallery"
            
            if chat_type in ["group", "supergroup"]:
                reply_text = f"🎞️ Диафильм 'Советское киноискусство 20-х годов'\n\nОткрыть: {short_url}"
            else:
                keyboard = {
                    "inline_keyboard": [[{
                        "text": "🎬 Открыть диафильм",
                        "web_app": {"url": WEB_APP_URL}
                    }]]
                }
                reply_text = "🎞️ Диафильм 'Советское киноискусство 20-х годов'\n\nНажми на кнопку ниже:"
            
            data = {
                "chat_id": chat_id,
                "text": reply_text
            }
            
            if chat_type not in ["group", "supergroup"]:
                data["reply_markup"] = keyboard
            
            requests.post(f"{TELEGRAM_API}/sendMessage", json=data)
    
    return "ok", 200

@app.route("/")
def index():
    return "Bot is running"
