import os
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        ACCESS_KEY=os.getenv("ACCESS_KEY"),
        RANDOM_URL="https://api.unsplash.com/photos/random",
        STATIC_FOLDER="static",
    )
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.static_folder, exist_ok=True)

    from . import routes

    app.register_blueprint(routes.bp)

    return app
