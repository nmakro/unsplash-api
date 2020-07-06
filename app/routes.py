from flask import Blueprint, redirect, url_for, render_template, current_app, request
from app.forms import SearchForm
from app.utils import save_image, ImageSaveError
import requests

bp = Blueprint("route", __name__)


@bp.route('/', methods=["GET", "POST"])
def home():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for("route.photo", search_param=search_form.select.data, data=search_form.search.data))
    return render_template("base.html", form=search_form)


@bp.route('/photo', methods=["GET", "POST"])
def photo():
    query = None
    try:
        query = {"query": {f"{request.args['search_param'].lower()}:{request.args['data']}"}}
    except KeyError:
        pass
    auth_headers = {"Authorization": f"Client-ID {current_app.config['ACCESS_KEY']}", "Accept-Version": "v1"}
    res = requests.get(current_app.config["RANDOM_URL"], headers=auth_headers, params=query) \
        if query is not None else requests.get(current_app.config["RANDOM_URL"], headers=auth_headers)
    if res.status_code == 200:
        try:
            img_url = res.json()["urls"]["small"]
            h = requests.head(img_url)
            content_type = h.headers.get("content-type")
            if content_type.lower() in ["image/jpg", "image/jpeg", "image/png"]:
                r = requests.get(img_url)
                if r.status_code == 200:
                    file_ext = content_type.split("/")[1]
                    file_name = res.json()["id"] + "." + file_ext
                    save_image(img_name=file_name, img_content=r.content)
                    return render_template("photo.html", filename=file_name)
            else:
                return render_template("415.html"), 415
        except (KeyError, OSError, ImageSaveError, Exception):
            return render_template("500.html"), 500
    elif res.status_code == 404:
        return render_template("404.html"), 404
    else:
        return render_template("external_error.html"), res.status_code
