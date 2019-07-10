from . import bot_api
from flask import request
from app.logger import log
from app import token
from app import telegram_bot
import telegram


@log.catch
@bot_api.route(f"/{token}", methods=["POST"])
def response():

    pass