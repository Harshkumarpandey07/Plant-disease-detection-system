
# ============================================================
#  PhytoSense — Irrigation ML Engine + Risk Calculator
#  backend/utils/irrigation_ml.py
# ============================================================

from datetime import datetime, timedelta


# ── Crop Water Needs (mm/day at peak ET) ───────────────────
CROP_WATER_NEEDS = {
    "Tomato":      5.5,
    "Potato":      4.5,
    "Corn":        6.0,
    "Rice":        8.0,
    "Wheat":       4.0,
    "Soybean":     5.0,
    "Cotton":      6.5,
    "Sugarcane":   7.0,
    "Onion":       4.0,
    "Pepper":      5.0,
    "Eggplant":    5.0,
    "Cucumber":    5.5,
    "Watermelon":  5.0,
    "Apple":       4.5,
    "Grape":       4.0,
    "Default":     5.0,
}

# ── Soil Water Holding Capacity Multipliers ─────────────────
SOIL_WHC = {
    "Clay":        1.0,
    "Clay Loam":   0.9,
    "Loam":        0.8,
    "Sandy Loam":  0.65,
    "Sandy":       0.45,
    "Silty Clay":  0.95,
    "Silt Loam":   0.85,
    "Default":     0.8,
}

# ── Growth Stage Crop Coefficients (FAO-56) ─────────────────
GROWTH_STAGE_KC = {
    "Seedling":   0.40,
    "Vegetative": 0.70,
    "Flowering":  1.05,
    "Fruiting":   1.20,
    "Harvest":    0.80,
    "Dormant":    0.30,
    "Default":    0.70,
}


# ============================================================
#  ET-Based Irrigation Schedule Calculator
# ============================================================

def calculate_irrigation_schedule(
    crop:         str,
    soil_type:    str,
    growth_stage: str,
    area_ha:      float,
    temperature:  float,
    humidity:     float,
    rainfall_7d:  float = 0.0,
) -> dict:
    """
    Generates a 7-day irrigation schedule using a simplified
    Penman-Monteith ET model adjusted for crop coefficient and
    soil water-holding capacity per FAO-56 guidelines.
    """

    # ── Lookup parameters ──────────────────────────────────
    base_et   = CROP_WATER_NEEDS.get(crop, CROP_WATER_NEEDS["Default"])
    kc        = GROWTH_STAGE_KC.get(growth_stage, GROWTH_STAGE_KC["Default"])
    whc       = SOIL_WHC.get(soil_type, SOIL_WHC["Default"])

    # ── ET₀ temperature + humidity correction ──────────────
    temp_factor  = 1.0 + max(0, (temperature - 25) * 0.025)
    humid_factor = 1.0 - max(0, (humidity - 60) * 0.005)
    et0          = base_et * temp_factor * humid_factor

    # ── Crop ET (ETc = ET0 x Kc) ───────────────────────────
    etc = et0 * kc

    # ── Daily rainfall offset (80% efficiency) ──────────────
    daily_rain = (rainfall_7d / 7) * 0.80

    # ── Net daily irrigation need ───────────────────────────
    net_daily = max(0, etc - daily_rain)

    # ── Volume per day (m³) ────────────────────────────────
    volume_m3 = (net_daily / 1000) * area_ha * 10000

    # ── Optimal timing based on temperature ────────────────
    if temperature > 30:
        optimal_time = "06:00 — 08:00 (early morning to minimise evaporation)"
    elif temperature > 22:
        optimal_time = "06:00 — 09:00 or 17:00 — 19:00"
    else:
        optimal_time = "14:00 — 16:00 (afternoon when soil is warm)"

    # ── Build 7-day schedule ───────────────────────────────
    schedule = []
    today     = datetime.utcnow()

    for i in range(7):
        day        = today + timedelta(days=i)
        irrigate   = net_daily > 0.5
        day_volume = round(volume_m3, 2) if irrigate else 0.0

        # Reduce volume on rainy days
        rain_today = round(daily_rain * 7 / max(daily_rain, 0.1), 1) if daily_rain > 0 and i < 2 else 0
        effective_volume = max(0, day_volume - rain_today * 0.001 * area_ha * 10000)

        schedule.append({
            "day":          day.strftime("%A"),
            "date":         day.strftime("%Y-%m-%d"),
            "irrigate":     irrigate,
            "volume_m3":    round(effective_volume, 2),
            "depth_mm":     round(net_daily, 1),
            "optimal_time": optimal_time if irrigate else "No irrigation needed",
            "notes":        _get_day_notes(i, temperature, humidity, growth_stage),
        })

    return {
        "crop":           crop,
        "soil_type":      soil_type,
        "growth_stage":   growth_stage,
        "area_ha":        area_ha,
        "et0_mm_day":     round(et0, 2),
        "etc_mm_day":     round(etc, 2),
        "kc":             kc,
        "net_daily_mm":   round(net_daily, 2),
        "weekly_volume_m3": round(sum(d["volume_m3"] for d in schedule), 2),
        "optimal_time":   optimal_time,
        "schedule":       schedule,
        "generated_at":   today.isoformat(),
    }


def _get_day_notes(day_index: int, temp: float, humidity: float, stage: str) -> str:
    notes = []
    if temp > 35:
        notes.append("Extreme heat — consider double irrigation")
    if humidity > 85:
        notes.append("High humidity — watch for fungal disease")
    if stage == "Flowering":
        notes.append("Critical stage — do not allow water stress")
    if stage == "Fruiting":
        notes.append("Consistent moisture prevents blossom-end rot")
    if day_index == 0:
        notes.append("Today's recommendation")
    return "; ".join(notes) if notes else "Normal conditions"


# ============================================================
#  Disease Outbreak Risk Index (DORI)
# ============================================================

def calculate_disease_risk(
    temperature: float,
    humidity:    float,
    rainfall_mm: float,
    crop:        str = "Tomato",
) -> dict:
    """
    Computes spatiotemporal Disease Outbreak Risk Index (DORI)
    from meteorological observations as described in the paper.
    Score range: 0-100 mapping to Low / Moderate / High / Severe.
    """

    # ── Temperature suitability (max 30 pts) ───────────────
    if 15 <= temperature <= 30:
        temp_score = 30
    elif 10 <= temperature <= 35:
        temp_score = 15
    else:
        temp_score = 0

    # ── Humidity susceptibility (max 40 pts) ───────────────
    if humidity >= 90:
        humidity_score = 40
    elif humidity >= 75:
        humidity_score = 25
    elif humidity >= 60:
        humidity_score = 10
    else:
        humidity_score = 0

    # ── Precipitation intensity (max 30 pts) ───────────────
    if rainfall_mm >= 10:
        rain_score = 30
    elif rainfall_mm >= 3:
        rain_score = 15
    elif rainfall_mm > 0:
        rain_score = 5
    else:
        rain_score = 0

    dori = temp_score + humidity_score + rain_score

    # ── Risk strata ────────────────────────────────────────
    if dori >= 80:
        level    = "Severe"
        color    = "#d32f2f"
        action   = "Immediate fungicide application required. Scout daily. Consider emergency treatment."
        scouting = "Daily"
    elif dori >= 55:
        level    = "High"
        color    = "#f57c00"
        action   = "Apply protective fungicide within 24-48 hours. Increase scouting frequency."
        scouting = "Every 2 days"
    elif dori >= 30:
        level    = "Moderate"
        color    = "#fbc02d"
        action   = "Monitor closely. Prepare fungicide application. Scout twice weekly."
        scouting = "Twice weekly"
    else:
        level    = "Low"
        color    = "#388e3c"
        action   = "Conditions not favourable for major disease outbreaks. Continue routine monitoring."
        scouting = "Weekly"

    # ── Most likely pathogens at risk ─────────────────────
    pathogens = _get_likely_pathogens(temperature, humidity, rainfall_mm, crop)

    return {
        "dori_score":      dori,
        "risk_level":      level,
        "color":           color,
        "action":          action,
        "scouting_freq":   scouting,
        "components": {
            "temperature_score": temp_score,
            "humidity_score":    humidity_score,
            "rainfall_score":    rain_score,
        },
        "likely_pathogens": pathogens,
        "conditions": {
            "temperature": temperature,
            "humidity":    humidity,
            "rainfall_mm": rainfall_mm,
        },
    }


def _get_likely_pathogens(temp: float, humidity: float, rain: float, crop: str) -> list:
    pathogens = []

    if humidity >= 90 and 10 <= temp <= 25:
        pathogens.append({
            "name":     "Phytophthora infestans (Late Blight)",
            "risk":     "High",
            "crops":    ["Tomato", "Potato"],
        })

    if humidity >= 75 and 24 <= temp <= 29:
        pathogens.append({
            "name":     "Alternaria solani (Early Blight)",
            "risk":     "Moderate",
            "crops":    ["Tomato", "Potato"],
        })

    if humidity >= 85 and temp >= 20:
        pathogens.append({
            "name":     "Xanthomonas spp. (Bacterial Spot)",
            "risk":     "Moderate",
            "crops":    ["Tomato", "Pepper", "Peach"],
        })

    if 15 <= temp <= 30 and rain > 0:
        pathogens.append({
            "name":     "Puccinia sorghi (Common Rust)",
            "risk":     "Moderate",
            "crops":    ["Corn"],
        })

    if humidity >= 80 and 20 <= temp <= 28:
        pathogens.append({
            "name":     "Guignardia bidwellii (Black Rot)",
            "risk":     "High",
            "crops":    ["Grape"],
        })

    # Filter to crop-relevant pathogens
    relevant = [p for p in pathogens if crop in p["crops"]]
    return relevant if relevant else pathogens[:2]


# ============================================================
#  Composite Crop Health Score
# ============================================================

def calculate_health_score(
    recent_scans:   list,
    dori_score:     float,
    soil_moisture:  float = 60.0,
) -> dict:
    """
    Computes a composite crop health score (0-100) from:
    - Recent scan history (disease prevalence and severity)
    - Current disease outbreak risk (DORI)
    - Estimated soil moisture level
    """

    # ── Scan history component (max 50 pts) ────────────────
    if not recent_scans:
        scan_score = 40
    else:
        total         = len(recent_scans)
        healthy_count = sum(1 for s in recent_scans if s.get("is_healthy", False))
        healthy_ratio = healthy_count / total

        severity_penalty = 0
        for scan in recent_scans:
            sev = scan.get("severity", "medium")
            if sev == "high":
                severity_penalty += 10
            elif sev == "medium":
                severity_penalty += 5
            else:
                severity_penalty += 1

        scan_score = max(0, (healthy_ratio * 50) - (severity_penalty / total))

    # ── Disease risk component (max 30 pts) ────────────────
    risk_score = max(0, 30 - (dori_score * 0.3))

    # ── Soil moisture component (max 20 pts) ───────────────
    if 50 <= soil_moisture <= 80:
        moisture_score = 20
    elif 35 <= soil_moisture <= 90:
        moisture_score = 12
    else:
        moisture_score = 5

    total_score = round(min(100, scan_score + risk_score + moisture_score))

    # ── Grade ──────────────────────────────────────────────
    if total_score >= 80:
        grade       = "Excellent"
        color       = "#388e3c"
        description = "Your crop is in excellent health. Continue current management practices."
    elif total_score >= 60:
        grade       = "Good"
        color       = "#689f38"
        description = "Crop health is good with minor concerns. Monitor closely and maintain schedule."
    elif total_score >= 40:
        grade       = "Fair"
        color       = "#fbc02d"
        description = "Some health concerns detected. Review recent scan results and weather risk."
    else:
        grade       = "Poor"
        color       = "#d32f2f"
        description = "Significant health concerns. Immediate field inspection and intervention recommended."

    return {
        "score":       total_score,
        "grade":       grade,
        "color":       color,
        "description": description,
        "components": {
            "scan_health":    round(scan_score),
            "disease_risk":   round(risk_score),
            "soil_moisture":  round(moisture_score),
        },
    }
