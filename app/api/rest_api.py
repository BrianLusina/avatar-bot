from . import bot_api
from flask import request, jsonify
from app.logger import log
from app import token
from app import telegram_bot
import re
import telegram


@log.catch
@bot_api.route(f"/{token}", methods=["POST"])
def response():
    update = telegram.Update.de_json(request.get_json(), telegram_bot)

    chat_id = update.message.chat.id
    message_id = update.message.message_id

    text = update.message.text.unicode("utf-8").decode()

    if text == "/start":
        bot_welcome = """Welcome to Avatar bot, the bot is using the service from http://avatars.adorable.io/ to 
        generate cool looking avatars based on the name you enter so please enter a name and the bot will reply with 
        an avatar for your name. """
        # send the welcoming message
        telegram_bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=message_id)

    else:
        try:
            # clear the message we got from any non alphabets
            text = re.sub(r"\W", "_", text)

            # create the api link for the avatar based on http://avatars.adorable.io/
            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())

            # reply with a photo to the name the user sent,
            # note that you can send photos by url and telegram will fetch it for you
            telegram_bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=message_id)

        except Exception as e:
            log.error(f"Failed to generate response with error {e}")
            # if things went wrong
            telegram_bot.sendMessage(chat_id=chat_id,
                                     text="There was a problem in the name you used, please enter different name",
                                     reply_to_message_id=message_id)

    return jsonify(dict(message="ok")), 200
