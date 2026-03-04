
# ============================================================
#  PhytoSense — User Profile Routes
#  backend/routes/user.py
# ============================================================

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from models.db import db
from models.user import User
from models.farm import Farm, Scan

user_bp = Blueprint("user", __name__)


# ── GET /api/user/profile ───────────────────────────────────
@user_bp.route("/user/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": user.to_dict()}), 200


# ── PUT /api/user/profile ───────────────────────────────────
@user_bp.route("/user/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """
    Update user personal info and/or farm profile.
    Accepts partial updates — only provided fields are changed.
    """
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True) or {}

    # ── Update user fields ─────────────────────────────────
    if "full_name" in data and data["full_name"].strip():
        user.full_name = data["full_name"].strip()

    if "phone" in data:
        user.phone = data["phone"]

    if "password" in data:
        if len(data["password"]) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400
        user.set_password(data["password"])

    # ── Update farm fields ─────────────────────────────────
    farm = user.farm
    if not farm:
        farm         = Farm(user_id=user.id)
        db.session.add(farm)

    farm_fields = [
        "farm_name", "latitude", "longitude", "location_str",
        "area_hectares", "primary_crop", "soil_type", "growth_stage",
        "notify_disease", "notify_irrigation", "notify_weather", "notify_weekly",
    ]

    for field in farm_fields:
        if field in data:
            setattr(farm, field, data[field])

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully",
        "user":    user.to_dict(),
    }), 200


# ── GET /api/user/stats ─────────────────────────────────────
@user_bp.route("/user/stats", methods=["GET"])
@jwt_required()
def get_user_stats():
    """
    Returns personalised statistics for the user dashboard:
    total scans, healthy rate, most scanned crop,
    most detected disease, scan streak and more.
    """
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    total    = Scan.query.filter_by(user_id=user_id).count()
    healthy  = Scan.query.filter_by(user_id=user_id, is_healthy=True).count()
    diseased = total - healthy

    # Most scanned crop
    top_crop = (
        db.session.query(Scan.crop_name, func.count(Scan.id).label("c"))
        .filter_by(user_id=user_id)
        .group_by(Scan.crop_name)
        .order_by(func.count(Scan.id).desc())
        .first()
    )

    # Most detected disease
    top_disease = (
        db.session.query(Scan.disease_name, func.count(Scan.id).label("c"))
        .filter_by(user_id=user_id, is_healthy=False)
        .group_by(Scan.disease_name)
        .order_by(func.count(Scan.id).desc())
        .first()
    )

    # Average confidence
    avg_conf = (
        db.session.query(func.avg(Scan.confidence))
        .filter_by(user_id=user_id)
        .scalar()
    )

    # Scans this month
    from datetime import datetime
    now        = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0)
    this_month  = (
        Scan.query
        .filter_by(user_id=user_id)
        .filter(Scan.scanned_at >= month_start)
        .count()
    )

    # Severity breakdown
    severity_counts = {}
    for sev in ["healthy", "low", "medium", "high"]:
        severity_counts[sev] = Scan.query.filter_by(
            user_id=user_id, severity=sev
        ).count()

    # Days active — days with at least one scan
    active_days = (
        db.session.query(func.date(Scan.scanned_at))
        .filter_by(user_id=user_id)
        .distinct()
        .count()
    )

    return jsonify({
        "total_scans":       total,
        "healthy_scans":     healthy,
        "diseased_scans":    diseased,
        "health_rate":       round((healthy / total * 100), 1) if total > 0 else 0,
        "avg_confidence":    round(float(avg_conf or 0) * 100, 1),
        "top_crop":          top_crop[0]    if top_crop    else None,
        "top_disease":       top_disease[0] if top_disease else None,
        "scans_this_month":  this_month,
        "severity_breakdown": severity_counts,
        "days_active":       active_days,
        "member_since":      user.created_at.strftime("%B %Y"),
    }), 200


# ── DELETE /api/user/account ────────────────────────────────
@user_bp.route("/user/account", methods=["DELETE"])
@jwt_required()
def delete_account():
    """
    Permanently deletes the user account, all scans
    and uploaded images. Requires password confirmation.
    """
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data     = request.get_json(silent=True) or {}
    password = data.get("password", "")

    if not user.check_password(password):
        return jsonify({"error": "Incorrect password"}), 403

    # Delete uploaded scan images from disk
    import os
    from flask import current_app
    for scan in user.scans:
        image_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], scan.image_filename
        )
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "message": "Account permanently deleted. We are sorry to see you go."
    }), 200
