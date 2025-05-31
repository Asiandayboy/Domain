from flask import Blueprint, jsonify
import os
from flasgger import swag_from


uids_bp = Blueprint("uids", __name__)


import os

model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "static", "assets", "3d"))


@uids_bp.route("/models", methods=["GET"])
@swag_from({
    "responses": {
        "200": {
            "description": "JSON array of strings of 3D model uids",
            "examples": {
                "application/json": {
                    "response": ["ID_1", "ID_2", "ID_3", "ID_4"]
                }
            }
        },
    } 
})
def get_model_list():
    """
    Get a list of available 3D model UIDs from SketchFab.
    ___ 
    """
    model_uids = [
        d for d in os.listdir(model_dir)
        if os.path.isdir(os.path.join(model_dir, d))
    ]

    return jsonify(model_uids)