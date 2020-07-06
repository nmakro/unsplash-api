import os
import requests
import json
from flask import jsonify, request, current_app
from app.api import bp
from app.utils import create_query, is_image, save_image, validate_query, ImageSaveError


@bp.route("/search", methods=["GET"])
def get_photo():
    incoming_query = request.args.to_dict()

    valid, msg = validate_query(incoming_query)
    if not valid:
        response = jsonify(msg)
        response.status_code = 400
        return response

    outgoing_query = {}
    if incoming_query:
        for k, v in incoming_query.items():
            outgoing_query = create_query(search_param=k, data=v)
    auth_headers = {
        "Authorization": f"Client-ID {current_app.config['ACCESS_KEY']}",
        "Accept-Version": "v1",
    }
    res = (
        requests.get(
            current_app.config["RANDOM_URL"],
            headers=auth_headers,
            params=outgoing_query,
        )
        if outgoing_query
        else requests.get(current_app.config["RANDOM_URL"], headers=auth_headers)
    )
    if res.status_code == 200:
        try:
            img_url = res.json()["urls"]["small"]
            h = requests.head(img_url)
            content_type = h.headers.get("content-type")
            if is_image(content_type):
                r = requests.get(img_url)
                if r.status_code == 200:
                    file_ext = content_type.split("/")[1]
                    file_name = res.json()["id"] + "." + file_ext
                    save_image(img_name=file_name, img_content=r.content)
                    payload = {
                        "thumb_url": os.path.join(
                            "http://localhost:5000/static", file_name
                        ),
                        "message": "Click on the link provided to view a thumbnail of the photo",
                    }
                    response = jsonify(payload)
                    return response
        except (ImageSaveError, KeyError):
            response = {"status_code": 500}
            return response
    elif res.status_code == 404:
        payload = {
            "message": "Please try again with a different search.",
            "error": res.json()["errors"],
        }
        response = jsonify(payload)
        response.status_code = 404
        return response
    else:
        payload = {
            "message": "An error occurred while trying to communicate with the external server. Please check the error message and try again",
            "error": res.json()["errors"],
        }
        response = jsonify(payload)
        response.status_code = res.status_code
        return response
