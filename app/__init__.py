import os
from flask import Flask


# import logging
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True
# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1

colors = ["red", "blue", "green"]


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        ACCESS_KEY=os.getenv("ACCESS_KEY"),
        RANDOM_URL="https://api.unsplash.com/photos/random",
        STATIC_FOLDER="static"
    )
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.static_folder, exist_ok=True)

    from . import routes
    app.register_blueprint(routes.bp)

    return app
