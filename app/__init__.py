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
        MEDIA_FILE="static"
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import routes
    app.register_blueprint(routes.bp)

    return app
