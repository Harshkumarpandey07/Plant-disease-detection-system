
# ============================================================
#  PhytoSense — Disease Encyclopedia Routes
#  backend/routes/disease_info.py
# ============================================================

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from utils.disease_db import get_disease_info, get_all_diseases, DISEASE_DB

disease_bp = Blueprint("disease", __name__)


# ── GET /api/disease ────────────────────────────────────────
@disease_bp.route("/disease", methods=["GET"])
@jwt_required()
def list_diseases():
    """
    Returns all 38 disease classes with basic info.
    Optional filters: crop, severity_class, healthy
    """
    crop           = request.args.get("crop",           None)
    severity_class = request.args.get("severity_class", None)
    healthy        = request.args.get("healthy",        None)
    search         = request.args.get("search",         None)

    diseases = get_all_diseases()

    if crop:
        diseases = [d for d in diseases if crop.lower() in d["crop"].lower()]

    if severity_class:
        diseases = [d for d in diseases if d["severity_class"].lower() == severity_class.lower()]

    if healthy is not None:
        is_healthy = healthy.lower() == "true"
        diseases   = [
            d for d in diseases
            if ("Healthy" in d["name"]) == is_healthy
        ]

    if search:
        term     = search.lower()
        diseases = [
            d for d in diseases
            if term in d["name"].lower() or term in d["crop"].lower()
        ]

    # Group by crop for organised response
    grouped = {}
    for d in diseases:
        crop_key = d["crop"]
        if crop_key not in grouped:
            grouped[crop_key] = []
        grouped[crop_key].append(d)

    return jsonify({
        "diseases":       diseases,
        "grouped":        grouped,
        "total":          len(diseases),
        "crops_covered":  sorted(grouped.keys()),
    }), 200


# ── GET /api/disease/<name> ─────────────────────────────────
@disease_bp.route("/disease/<path:disease_name>", methods=["GET"])
@jwt_required()
def get_disease(disease_name):
    """
    Full disease profile: symptoms, causes,
    organic treatment, chemical treatment, prevention.
    Supports fuzzy name matching.
    """
    info = get_disease_info(disease_name)

    if not info:
        return jsonify({"error": f"Disease '{disease_name}' not found"}), 404

    # Attach severity colour for frontend display
    severity_colors = {
        "High":   "#d32f2f",
        "Medium": "#f57c00",
        "Low":    "#fbc02d",
        "None":   "#388e3c",
    }

    info["severity_color"] = severity_colors.get(
        info.get("severity_class", "None"), "#888888"
    )

    return jsonify({
        "disease":     disease_name,
        "info":        info,
    }), 200


# ── GET /api/disease/crop/<crop_name> ───────────────────────
@disease_bp.route("/disease/crop/<crop_name>", methods=["GET"])
@jwt_required()
def get_diseases_by_crop(crop_name):
    """
    Returns all diseases for a specific crop.
    """
    matches = {
        name: info
        for name, info in DISEASE_DB.items()
        if crop_name.lower() in info["crop"].lower()
    }

    if not matches:
        return jsonify({
            "error":     f"No diseases found for crop '{crop_name}'",
            "available": sorted(set(v["crop"] for v in DISEASE_DB.values())),
        }), 404

    result = []
    for name, info in matches.items():
        result.append({
            "name":            name,
            "crop":            info["crop"],
            "scientific_name": info["scientific_name"],
            "severity_class":  info["severity_class"],
            "description":     info["description"],
            "symptoms":        info["symptoms"],
            "prevention":      info["prevention"],
        })

    return jsonify({
        "crop":     crop_name,
        "diseases": result,
        "total":    len(result),
    }), 200


# ── GET /api/disease/summary/crops ──────────────────────────
@disease_bp.route("/disease/summary/crops", methods=["GET"])
@jwt_required()
def crop_summary():
    """
    Returns summary of disease coverage per crop.
    Useful for the encyclopedia index page.
    """
    summary = {}
    for name, info in DISEASE_DB.items():
        crop = info["crop"]
        if crop not in summary:
            summary[crop] = {
                "crop":         crop,
                "total":        0,
                "diseases":     0,
                "healthy":      0,
                "high_risk":    0,
            }
        summary[crop]["total"] += 1
        if "Healthy" in name:
            summary[crop]["healthy"] += 1
        else:
            summary[crop]["diseases"] += 1
        if info["severity_class"] == "High":
            summary[crop]["high_risk"] += 1

    return jsonify({
        "crops":   list(summary.values()),
        "total_diseases": len(DISEASE_DB),
        "total_crops":    len(summary),
    }), 200
