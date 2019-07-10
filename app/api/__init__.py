# flake8: noqa
from flask import Blueprint


bot_api = Blueprint(
    name="Callback",
    import_name=__name__,
    url_prefix=f"/api/avatar-bot",
    static_folder="static",
    template_folder="templates",
)

from . import rest_api
