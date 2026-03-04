
# ============================================================
#  PhytoSense — Prediction Routes
#  backend/routes/predict.py
# ============================================================

import os
import uuid
import base64
import json
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.db import db
from models.farm import Scan
from models.user import User
from utils.ml_model import predict
from utils.disease_db import get_disease_info

predict_bp = Blueprint("predict", __name__)


def _allowed_file(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def _save_scan(user_id, result, filename, source, weather=None, lat=None, lon=None):
    """Persist a scan result to the database."""
    scan = Scan(
        user_id        = user_id,
        image_filename = filename,
        source         = source,
        disease_name   = result["disease_name"],
        crop_name      = result["crop_name"],
        confidence     = result["confidence"],
        is_healthy     = result["is_healthy"],
        severity       = result["severity"],
        top3_json      = json.dumps(result["top3"]),
        temperature    = weather.get("temperature") if weather else None,
        humidity       = weather.get("humidity")    if weather else None,
        weather_desc   = weather.get("description") if weather else None,
        latitude       = lat,
        longitude      = lon,
    )
    db.session.add(scan)
    db.session.commit()
    return scan


# ── POST /api/predict ───────────────────────────────────────
@predict_bp.route("/predict", methods=["POST"])
@jwt_required()
def predict_upload():
    """
    Accept a multipart/form-data image upload.
    Run CNN inference and return disease prediction.
    """
    user_id = int(get_jwt_identity())

    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not _allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Use JPG, PNG, WEBP or BMP"}), 415

    # Save image
    ext      = file.filename.rsplit(".", 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Run inference
    result = predict(
        image_path       = filepath,
        model_path       = current_app.config["MODEL_PATH"],
        class_names_path = current_app.config["CLASS_NAMES_PATH"],
        img_size         = current_app.config["IMG_SIZE"],
    )

    # Enrich with disease knowledge base
    disease_info = get_disease_info(result["disease_name"])

    # Optional weather context from request body
    weather = request.form.get("weather")
    weather = json.loads(weather) if weather else None
    lat     = request.form.get("latitude",  type=float)
    lon     = request.form.get("longitude", type=float)

    # Persist scan
    scan = _save_scan(user_id, result, filename, "upload", weather, lat, lon)

    return jsonify({
        "scan_id":    scan.id,
        "prediction": {
            **result,
            "disease_info": disease_info,
        },
        "image_url":  f"/static/uploads/{filename}",
        "scanned_at": scan.scanned_at.isoformat(),
    }), 200


# ── POST /api/predict/camera ────────────────────────────────
@predict_bp.route("/predict/camera", methods=["POST"])
@jwt_required()
def predict_camera():
    """
    Accept a base64-encoded image from the camera stream.
    Run CNN inference and return disease prediction.
    """
    user_id = int(get_jwt_identity())
    data    = request.get_json(silent=True) or {}

    image_b64 = data.get("image_base64")
    if not image_b64:
        return jsonify({"error": "No image_base64 field provided"}), 400

    # Strip data URL prefix if present
    if "," in image_b64:
        image_b64 = image_b64.split(",", 1)[1]

    try:
        image_bytes = base64.b64decode(image_b64)
    except Exception:
        return jsonify({"error": "Invalid base64 image data"}), 400

    # Save decoded image
    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    with open(filepath, "wb") as f:
        f.write(image_bytes)

    # Run inference
    result = predict(
        image_path       = filepath,
        model_path       = current_app.config["MODEL_PATH"],
        class_names_path = current_app.config["CLASS_NAMES_PATH"],
        img_size         = current_app.config["IMG_SIZE"],
    )

    # Enrich with disease knowledge base
    disease_info = get_disease_info(result["disease_name"])

    # Optional weather + location context
    weather = data.get("weather")
    lat     = data.get("latitude")
    lon     = data.get("longitude")

    # Persist scan
    scan = _save_scan(user_id, result, filename, "camera", weather, lat, lon)

    return jsonify({
        "scan_id":    scan.id,
        "prediction": {
            **result,
            "disease_info": disease_info,
        },
        "image_url":  f"/static/uploads/{filename}",
        "scanned_at": scan.scanned_at.isoformat(),
    }), 200
