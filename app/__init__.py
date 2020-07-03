import os
from flask import Flask, redirect, render_template, url_for
from app.forms import SearchForm
from app.utils import thumb_image
import requests
from . import routes

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
        RANDOM_URL="https://api.unsplash.com/photos/random",
        MEDIA_FILE="static"
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=["GET", "POST"])
    def home():
        search = SearchForm()
        if search.validate_on_submit():
            return redirect(url_for("photo"))
        return render_template("base.html", form=search)

    @app.route('/photo', methods=["GET", "POST"])
    def photo():
        query_params = {"query": "color:green"}
        auth_headers = {"Authorization": f"Client-ID {app.config['ACCESS_KEY']}", "Accept-Version": "v1"}
        res = requests.get(app.config["RANDOM_URL"], headers=auth_headers, params=query_params)
        if res.status_code == 200:
            try:
                img_url = res.json()["urls"]["small"]
                h = requests.head(img_url)
                content_type = h.headers.get('content-type').lower()
                if content_type in ["image/jpg", "image/jpeg", "image/png"]:
                    r = requests.get(img_url)
                    if r.status_code == 200:
                        file_ext = content_type.split("/")[1]
                        print(file_ext)
                        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), app.config["MEDIA_FILE"], res.json()["id"] + "." + file_ext), "wb") as f:
                            f.write(r.content)
                        img_name = os.path.join(app.config["MEDIA_FILE"], res.json()["id"] + "." + file_ext)
                        thumb_image(os.path.join(os.path.dirname(os.path.abspath(__file__)), img_name))
                        return render_template("photo.html", filename=img_name)
            except KeyError:
                return None
            return redirect(img_url)

    @app.route('/<filename>', methods=["GET", "POST"])
    def show_thumbnail(filename):
        return render_template("thumb.html", image_thumb=filename)

    return app
