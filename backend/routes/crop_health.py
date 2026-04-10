
# ============================================================
#  PhytoSense — Crop Health Routes
#  backend/routes/crop_health.py
# ============================================================

import requests
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from models.farm import Scan
from utils.irrigation_ml import calculate_disease_risk, calculate_health_score

crop_health_bp = Blueprint("crop_health", __name__)


def _get_live_weather(lat: float, lon: float, api_key: str) -> dict:
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


# ── GET /api/crop/health ────────────────────────────────────
@crop_health_bp.route("/crop/health", methods=["GET"])
@jwt_required()
def get_crop_health():
    """
    Returns composite crop health score (0-100) computed from:
      - Recent scan history (last 30 scans)
      - Current Disease Outbreak Risk Index (DORI)
      - Estimated soil moisture from humidity proxy
    """
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    farm = user.farm

    # ── Fetch recent scans ─────────────────────────────────
    recent_scans_raw = (
        Scan.query
        .filter_by(user_id=user_id)
        .order_by(Scan.scanned_at.desc())
        .limit(30)
        .all()
    )

    recent_scans = [
        {
            "is_healthy": s.is_healthy,
            "severity":   s.severity,
            "confidence": s.confidence,
            "disease":    s.disease_name,
        }
        for s in recent_scans_raw
    ]

    # ── Get weather for DORI ───────────────────────────────
    api_key = current_app.config.get("OPENWEATHER_API_KEY", "")
    lat     = farm.latitude  if farm else 26.8467
    lon     = farm.longitude if farm else 80.9462
    crop    = farm.primary_crop if farm else "Tomato"

    if api_key and api_key != "YOUR_KEY_HERE":
        weather = _get_live_weather(lat, lon, api_key)
    else:
        weather = {"temperature": 28.0, "humidity": 65.0, "rainfall_1h": 0.0}

    # ── Compute DORI ───────────────────────────────────────
    risk = calculate_disease_risk(
        temperature = weather["temperature"],
        humidity    = weather["humidity"],
        rainfall_mm = weather["rainfall_1h"],
        crop        = crop,
    )

    # ── Soil moisture proxy from humidity ──────────────────
    soil_moisture = min(100, weather["humidity"] * 0.85)

    # ── Composite health score ─────────────────────────────
    health = calculate_health_score(
        recent_scans  = recent_scans,
        dori_score    = risk["dori_score"],
        soil_moisture = soil_moisture,
    )

    # ── Build scan summary ─────────────────────────────────
    total    = len(recent_scans)
    healthy  = sum(1 for s in recent_scans if s["is_healthy"])
    diseased = total - healthy

    top_issues = {}
    for s in recent_scans:
        if not s["is_healthy"]:
            top_issues[s["disease"]] = top_issues.get(s["disease"], 0) + 1

    top_issues_list = sorted(
        [{"disease": k, "count": v} for k, v in top_issues.items()],
        key=lambda x: x["count"],
        reverse=True,
    )[:3]

    return jsonify({
        "health":       health,
        "risk":         risk,
        "scan_summary": {
            "total":      total,
            "healthy":    healthy,
            "diseased":   diseased,
            "top_issues": top_issues_list,
        },
        "weather":      weather,
        "farm": {
            "name":         farm.farm_name    if farm else "My Farm",
            "crop":         farm.primary_crop if farm else "Tomato",
            "growth_stage": farm.growth_stage if farm else "Vegetative",
            "area_ha":      farm.area_hectares if farm else 1.0,
        },
    }), 200
