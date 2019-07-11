from time import sleep
from telegram.chataction import ChatAction
from app import telegram_bot
from app.logger import log
import re


@log.catch
def generate_smart_reply(text, chat_id, message_id):
    """
    Handles generating a smart reply
    :param text: Text from User
    :param chat_id: Chat id in conversation
    :param message_id: Message Id in conversation
    :return: True if the message is successfully sent, False otherwise
    :rtype: bool
    """

    if text == "/start":
        bot_welcome = """Welcome to Avatar bot, the bot is using the service from http://avatars.adorable.io/ to 
         generate cool looking avatars based on the name you enter so please enter a name and the bot will reply with 
         an avatar for your name. """
        # send the welcoming message
        telegram_bot.sendChatAction(chat_id=chat_id, action=ChatAction.TYPING)
        sleep(1.5)
        telegram_bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=message_id)
        return True
    else:
        try:
            # clear the message we got from any non alphabets
            text = re.sub(r"\W", "_", text)

            # create the api link for the avatar based on http://avatars.adorable.io/
            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())

            # reply with a photo to the name the user sent,
            # note that you can send photos by url and telegram will fetch it for you
            telegram_bot.sendChatAction(chat_id=chat_id, action=ChatAction.UPLOAD_PHOTO)
            sleep(2)
            telegram_bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=message_id)
            return True
        except Exception as e:
            log.error(f"Failed to generate response with error {e}")
            # if things went wrong
            telegram_bot.sendMessage(chat_id=chat_id,
                                     text="There was a problem in the name you used, please enter different name",
                                     reply_to_message_id=message_id)
            return False
