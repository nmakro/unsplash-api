from flask import Blueprint, redirect, url_for, render_template, current_app
from app.forms import SearchForm
from app.utils import thumb_image
import requests
import os

bp = Blueprint("route", __name__)


@bp.route('/', methods=["GET", "POST"])
def home():
    search = SearchForm()
    if search.validate_on_submit():
        return redirect(url_for("route.photo"))
    return render_template("base.html", form=search)


@bp.route('/photo', methods=["GET", "POST"])
def photo():
    query_params = {"query": "color:green"}
    auth_headers = {"Authorization": f"Client-ID {current_app.config['ACCESS_KEY']}", "Accept-Version": "v1"}
    res = requests.get(current_app.config["RANDOM_URL"], headers=auth_headers, params=query_params)
    if res.status_code == 200:
        try:
            img_url = res.json()["urls"]["small"]
            h = requests.head(img_url)
            content_type = h.headers.get('content-type').lower()
            if content_type in ["image/jpg", "image/jpeg", "image/png"]:
                r = requests.get(img_url)
                if r.status_code == 200:
                    file_ext = content_type.split("/")[1]
                    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), current_app.config["MEDIA_FILE"], res.json()["id"] + "." + file_ext), "wb") as f:
                        f.write(r.content)
                    img_name = os.path.join(current_app.config["MEDIA_FILE"], res.json()["id"] + "." + file_ext)
                    thumb_image(os.path.join(os.path.dirname(os.path.abspath(__file__)), img_name))
                    return render_template("photo.html", filename=img_name)
        except KeyError:
            return None
        return redirect(img_url)


@bp.route('/<filename>', methods=["GET", "POST"])
def show_thumbnail(filename):
    return render_template("thumb.html", image_thumb=filename)
