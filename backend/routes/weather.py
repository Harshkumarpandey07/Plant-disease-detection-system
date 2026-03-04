
# ============================================================
#  PhytoSense — Weather Routes
#  backend/routes/weather.py
# ============================================================

import requests
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from utils.irrigation_ml import calculate_disease_risk

weather_bp = Blueprint("weather", __name__)


def _fetch_weather(lat: float, lon: float, api_key: str) -> dict:
    """Fetch current weather from OpenWeatherMap."""
    url    = f"{current_app.config['OPENWEATHER_BASE']}/weather"
    params = {
        "lat":   lat,
        "lon":   lon,
        "appid": api_key,
        "units": "metric",
    }
    resp = requests.get(url, params=params, timeout=8)
    resp.raise_for_status()
    return resp.json()


def _fetch_forecast(lat: float, lon: float, api_key: str) -> dict:
    """Fetch 5-day / 3-hour forecast from OpenWeatherMap."""
    url    = f"{current_app.config['OPENWEATHER_BASE']}/forecast"
    params = {
        "lat":   lat,
        "lon":   lon,
        "appid": api_key,
        "units": "metric",
        "cnt":   40,
    }
    resp = requests.get(url, params=params, timeout=8)
    resp.raise_for_status()
    return resp.json()


def _mock_weather(lat: float, lon: float) -> dict:
    """Deterministic mock weather for development."""
    return {
        "current": {
            "temperature":  28.4,
            "feels_like":   31.2,
            "humidity":     72,
            "pressure":     1008,
            "wind_speed":   3.2,
            "wind_dir":     180,
            "description":  "Partly cloudy",
            "icon":         "02d",
            "visibility":   8000,
            "uv_index":     6,
            "rainfall_1h":  0.0,
            "location":     "Lucknow, IN",
            "lat":          lat,
            "lon":          lon,
        },
        "forecast": [
            {
                "date":        f"Day {i+1}",
                "temp_max":    30 + i,
                "temp_min":    22 + i,
                "humidity":    70 + i * 2,
                "description": "Partly cloudy",
                "rainfall_mm": 0.0 if i < 3 else 5.0 * i,
                "icon":        "02d",
            }
            for i in range(7)
        ],
        "mock": True,
    }


def _parse_current(data: dict) -> dict:
    main    = data.get("main", {})
    weather = data.get("weather", [{}])[0]
    wind    = data.get("wind", {})
    rain    = data.get("rain",  {})

    return {
        "temperature":  main.get("temp"),
        "feels_like":   main.get("feels_like"),
        "humidity":     main.get("humidity"),
        "pressure":     main.get("pressure"),
        "wind_speed":   wind.get("speed"),
        "wind_dir":     wind.get("deg"),
        "description":  weather.get("description", "").capitalize(),
        "icon":         weather.get("icon"),
        "visibility":   data.get("visibility"),
        "rainfall_1h":  rain.get("1h", 0.0),
        "location":     data.get("name", ""),
        "lat":          data.get("coord", {}).get("lat"),
        "lon":          data.get("coord", {}).get("lon"),
    }


def _parse_forecast(data: dict) -> list:
    """Condense 3-hour slots into daily summaries."""
    from collections import defaultdict
    daily = defaultdict(list)

    for item in data.get("list", []):
        date = item["dt_txt"].split(" ")[0]
        daily[date].append(item)

    result = []
    for date, slots in list(daily.items())[:7]:
        temps    = [s["main"]["temp"]     for s in slots]
        humidity = [s["main"]["humidity"] for s in slots]
        rain     = sum(s.get("rain", {}).get("3h", 0) for s in slots)
        weather  = slots[len(slots)//2].get("weather", [{}])[0]

        result.append({
            "date":        date,
            "temp_max":    round(max(temps), 1),
            "temp_min":    round(min(temps), 1),
            "humidity":    round(sum(humidity) / len(humidity), 1),
            "description": weather.get("description", "").capitalize(),
            "rainfall_mm": round(rain, 1),
            "icon":        weather.get("icon", "01d"),
        })

    return result


# ── GET /api/weather ────────────────────────────────────────
@weather_bp.route("/weather", methods=["GET"])
@jwt_required()
def get_weather():
    """
    Returns current weather + 7-day forecast for given
    lat/lon. Falls back to user farm location if not provided.
    Uses mock data if no API key is configured.
    """
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)

    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    # Fall back to farm location
    if lat is None or lon is None:
        if user and user.farm:
            lat = user.farm.latitude
            lon = user.farm.longitude
        else:
            lat, lon = 26.8467, 80.9462

    api_key = current_app.config.get("OPENWEATHER_API_KEY", "")

    if not api_key or api_key == "YOUR_KEY_HERE":
        return jsonify(_mock_weather(lat, lon)), 200

    try:
        current_data  = _fetch_weather(lat, lon, api_key)
        forecast_data = _fetch_forecast(lat, lon, api_key)

        current  = _parse_current(current_data)
        forecast = _parse_forecast(forecast_data)

        return jsonify({
            "current":  current,
            "forecast": forecast,
            "mock":     False,
        }), 200

    except requests.exceptions.HTTPError as e:
        if e.response and e.response.status_code == 401:
            return jsonify({"error": "Invalid OpenWeatherMap API key"}), 401
        return jsonify(_mock_weather(lat, lon)), 200

    except Exception:
        return jsonify(_mock_weather(lat, lon)), 200


# ── GET /api/climate/risk ───────────────────────────────────
@weather_bp.route("/climate/risk", methods=["GET"])
@jwt_required()
def get_climate_risk():
    """
    Computes Disease Outbreak Risk Index (DORI) from
    current weather conditions as described in the paper.
    """
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)

    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    if lat is None and user and user.farm:
        lat = user.farm.latitude
        lon = user.farm.longitude
    else:
        lat = lat or 26.8467
        lon = lon or 80.9462

    crop    = request.args.get("crop", user.farm.primary_crop if user and user.farm else "Tomato")
    api_key = current_app.config.get("OPENWEATHER_API_KEY", "")

    # Get live or mock weather
    if api_key and api_key != "YOUR_KEY_HERE":
        try:
            raw     = _fetch_weather(lat, lon, api_key)
            current = _parse_current(raw)
            temp    = current["temperature"]
            humid   = current["humidity"]
            rain    = current["rainfall_1h"]
        except Exception:
            temp, humid, rain = 28.0, 72.0, 0.0
    else:
        temp, humid, rain = 28.0, 72.0, 0.0

    risk = calculate_disease_risk(
        temperature = temp,
        humidity    = humid,
        rainfall_mm = rain,
        crop        = crop,
    )

    return jsonify({
        "risk":    risk,
        "weather": {"temperature": temp, "humidity": humid, "rainfall_mm": rain},
        "crop":    crop,
        "lat":     lat,
        "lon":     lon,
    }), 200
