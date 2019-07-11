from . import bot_api
from flask import request, jsonify
from app.logger import log
from app import token
from app import telegram_bot
import telegram
from ..telebot.ai import generate_smart_reply


@log.catch
@bot_api.route(f"/{token}", methods=["POST"])
def response():
    update = telegram.Update.de_json(request.get_json(), telegram_bot)

    try:
        chat_id = update.message.chat.id
        message_id = update.message.message_id

        text = update.message.text.encode("utf-8").decode()

        result = generate_smart_reply(text=text, chat_id=chat_id, message_id=message_id)

        if result:
            return jsonify(dict(message="ok")), 200
        else:
            return jsonify(dict(message="failed")), 400
    except Exception as e:
        log.error(f"Failed with error {e}")
        return jsonify(dict(message="failed")), 400
