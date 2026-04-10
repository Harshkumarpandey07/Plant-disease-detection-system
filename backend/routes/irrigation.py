
# ============================================================
#  PhytoSense — Irrigation Routes
#  backend/routes/irrigation.py
# ============================================================

import requests
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from utils.irrigation_ml import calculate_irrigation_schedule

irrigation_bp = Blueprint("irrigation", __name__)


def _get_weather_data(lat: float, lon: float, api_key: str) -> dict:
    """Fetch current weather for ET calculation."""
    try:
        url    = f"{current_app.config['OPENWEATHER_BASE']}/weather"
        params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
        resp   = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data   = resp.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity":    data["main"]["humidity"],
            "rainfall_1h": data.get("rain", {}).get("1h", 0.0),
        }
    except Exception:
        return {"temperature": 28.0, "humidity": 65.0, "rainfall_1h": 0.0}


# ── POST /api/irrigation/predict ────────────────────────────
@irrigation_bp.route("/irrigation/predict", methods=["POST"])
@jwt_required()
def predict_irrigation():
    """
    Generate a 7-day ET-based irrigation schedule.
    Accepts custom parameters in the request body.
    Falls back to user farm profile defaults.
    """
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)
    data    = request.get_json(silent=True) or {}

    # Pull params — prefer request body, fall back to farm profile
    farm = user.farm if user else None

    crop         = data.get("crop",         farm.primary_crop   if farm else "Tomato")
    soil_type    = data.get("soil_type",    farm.soil_type      if farm else "Clay Loam")
    growth_stage = data.get("growth_stage", farm.growth_stage   if farm else "Vegetative")
    area_ha      = data.get("area_ha",      farm.area_hectares  if farm else 1.0)
    lat          = data.get("latitude",     farm.latitude       if farm else 26.8467)
    lon          = data.get("longitude",    farm.longitude      if farm else 80.9462)
    rainfall_7d  = data.get("rainfall_7d",  0.0)

    # Validate inputs
    if area_ha <= 0:
        return jsonify({"error": "Area must be greater than 0"}), 400

    # Get weather for ET calculation
    api_key = current_app.config.get("OPENWEATHER_API_KEY", "")
    if api_key and api_key != "YOUR_KEY_HERE":
        weather = _get_weather_data(lat, lon, api_key)
    else:
        weather = {
            "temperature": data.get("temperature", 28.0),
            "humidity":    data.get("humidity",    65.0),
            "rainfall_1h": 0.0,
        }

    temperature = weather["temperature"]
    humidity    = weather["humidity"]

    schedule = calculate_irrigation_schedule(
        crop         = crop,
        soil_type    = soil_type,
        growth_stage = growth_stage,
        area_ha      = area_ha,
        temperature  = temperature,
        humidity     = humidity,
        rainfall_7d  = rainfall_7d,
    )

    return jsonify({
        "schedule": schedule,
        "weather":  weather,
        "inputs": {
            "crop":         crop,
            "soil_type":    soil_type,
            "growth_stage": growth_stage,
            "area_ha":      area_ha,
            "lat":          lat,
            "lon":          lon,
        },
    }), 200


# ── GET /api/irrigation/schedule ────────────────────────────
@irrigation_bp.route("/irrigation/schedule", methods=["GET"])
@jwt_required()
def get_schedule():
    """
    Quick irrigation schedule using stored farm profile.
    No request body needed — uses farm defaults directly.
    """
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)

    if not user or not user.farm:
        return jsonify({"error": "Farm profile not found. Please complete your profile."}), 404

    farm    = user.farm
    api_key = current_app.config.get("OPENWEATHER_API_KEY", "")

    if api_key and api_key != "YOUR_KEY_HERE":
        weather = _get_weather_data(farm.latitude, farm.longitude, api_key)
    else:
        weather = {"temperature": 28.0, "humidity": 65.0, "rainfall_1h": 0.0}

    schedule = calculate_irrigation_schedule(
        crop         = farm.primary_crop,
        soil_type    = farm.soil_type,
        growth_stage = farm.growth_stage,
        area_ha      = farm.area_hectares,
        temperature  = weather["temperature"],
        humidity     = weather["humidity"],
        rainfall_7d  = 0.0,
    )

    return jsonify({
        "schedule": schedule,
        "weather":  weather,
        "farm": {
            "name":         farm.farm_name,
            "crop":         farm.primary_crop,
            "soil_type":    farm.soil_type,
            "growth_stage": farm.growth_stage,
            "area_ha":      farm.area_hectares,
        },
    }), 200
