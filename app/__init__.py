import logging
from flask import Flask, jsonify
from .config import config
import jinja2
from .logger import log as app_logger
import telegram
import os

token = os.environ.get("TOKEN")
telegram_bot = telegram.Bot(token=token)


class AvatarBot(Flask):
    """
     Custom application class subclassing Flask application. This is to ensure more modularity in
      terms of static files and templates. This way a module will have its own templates and the
       root template folder will be more modularized and easier to manage
     """

    def __init__(self):
        """
        jinja_loader object (a FileSystemLoader pointing to the global templates folder) is
        being replaced with a ChoiceLoader object that will first search the normal
        FileSystemLoader and then check a PrefixLoader that we create
        """
        Flask.__init__(self, __name__)
        self.jinja_loader = jinja2.ChoiceLoader(
            [self.jinja_loader, jinja2.PrefixLoader({}, delimiter=".")]
        )

    def create_global_jinja_loader(self):
        """
        Overriding to return the loader set up in __init__
        :return: jinja_loader
        """
        return self.jinja_loader

    def register_blueprint(self, blueprint, **options):
        """
        Overriding to add the blueprints names to the prefix loader's mapping
        :param blueprint:
        :param options:
        """
        Flask.register_blueprint(self, blueprint, **options)
        self.jinja_loader.loaders[1].mapping[blueprint.name] = blueprint.jinja_loader


def create_app(config_name):
    """
    Creates a new flask app instance with the given configuration
    :param config_name: configuration to use when creating the application
    :return: a new WSGI Flask app
    :rtype: Flask
    """
    app = AvatarBot()

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    error_handlers(app)
    register_app_blueprints(app)
    app_logger_handler(app, config_name)
    request_handlers(app)

    # this will reduce the load time for templates and increase the application performance
    app.jinja_env.cache = {}

    @app.route("/api/avatar-bot/health")
    def health():
        return jsonify({"message": "I am healthy :D"}), 200

    return app


def request_handlers(app_):
    """
    Handles before and after the requests handled by the application
    :param app: the current application
    """

    @app_.after_request
    def after_request(response):
        """
        Is handled afer each request and can be used to add headers to the response
        or handle further processing
        :param response: Response object that is sent back to client
        """
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response


def app_logger_handler(app, config_name):
    """
    Will handle error logging for the application and will store the app log files in a file that can
    later be accessed.
    :param config_name: configuration name
    :param app: current flask application
    """
    from logging.handlers import RotatingFileHandler

    if app.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    if config_name == "production":
        try:
            file_handler = RotatingFileHandler(
                filename="/home/avatar/app.log",
                mode="a",
                maxBytes=1 * 1024 * 1024,
                backupCount=10,
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%("
                    "lineno)d]"
                )
            )
            app.logger.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.info("App")

        except FileNotFoundError as fnfe:
            app_logger.error(
                "Failed to create rotating file handler in {CONFIG} environment with error {ERROR}".format(
                    CONFIG=config_name, ERROR=fnfe
                )
            )
            app.logger.info("App")


def error_handlers(app):
    """
    Error handlers function that will initialize error handling templates for the entire application
    :param app: the flask app
    """

    @app.errorhandler(404)
    def not_found(error):
        """
        This will handle errors that involve 404 messages
        :return: a template instructing user they have sent a request that does not exist on
         the server
        """
        app_logger.error(f"An error occurred during a request. Error => {error}")
        return jsonify(dict(message="Failed to find resource")), 404

    @app.errorhandler(500)
    def server_error(e):
        # Log the error and stacktrace.
        app_logger.error(f"An error occurred during a request. Error => {e}")
        return jsonify(dict(message=f"Request failed with error {e}")), 500

    @app.errorhandler(403)
    def error_403(error):
        app_logger.error(f"An error occurred during a request. Error => {error}")
        return jsonify(dict(message=f"Request failed with error {error}")), 403

    @app.errorhandler(400)
    def bad_request(error):
        app_logger.error(f"An error occurred during a request. Error => {error}")
        return jsonify(dict(message=f"Request failed with error {error}")), 400


def register_app_blueprints(app_):
    """
    Registers the application blueprints
    :param app_: the current flask app
    """
    from app.api import bot_api

    app_.register_blueprint(bot_api)
