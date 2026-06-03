from flask import Flask, request
import requests
import logging

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "6324068841:AAFziCaTU57gZ9PO8f9AY-7kL-YAFIglfDg"
BOT_USERNAME = "MarkBernesBot"  # Добавляем username бота
WEB_APP_URL = "https://devarlec.github.io/telega_m_bernesa/soviet_filv/"

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Bot is running"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    logger.info(f"Получен update: {update}")
    
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        chat_type = update["message"]["chat"]["type"]
        
        logger.info(f"Сообщение от chat_id={chat_id}, тип={chat_type}, текст={text}")
        
        # Проверяем команду (с @username или без)
        is_command = (
            text == "/sovietfilmhistory" or 
            text == f"/sovietfilmhistory@{BOT_USERNAME}"
        )
        
        if is_command:
            logger.info(f"Команда распознана! Отправляем ответ в chat_id={chat_id}")
            
            try:
                response = requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": f"Открыть галерею: {WEB_APP_URL}"
                    },
                    timeout=5
                )
                logger.info(f"Ответ от Telegram API: {response.status_code} - {response.text}")
            except Exception as e:
                logger.error(f"Ошибка при отправке: {e}")
    
    return "ok", 200
