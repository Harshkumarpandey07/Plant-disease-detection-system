
# ============================================================
#  PhytoSense — Scan History Routes
#  backend/routes/history.py
# ============================================================

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from models.db import db
from models.farm import Scan

history_bp = Blueprint("history", __name__)


# ── GET /api/history ────────────────────────────────────────
@history_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():
    """
    Paginated scan history with optional filters.
    Query params: page, per_page, crop, healthy, severity
    """
    user_id  = int(get_jwt_identity())
    page     = request.args.get("page",     1,     type=int)
    per_page = request.args.get("per_page", 10,    type=int)
    crop     = request.args.get("crop",     None)
    healthy  = request.args.get("healthy",  None)
    severity = request.args.get("severity", None)

    per_page = min(per_page, 50)

    query = Scan.query.filter_by(user_id=user_id)

    if crop:
        query = query.filter(Scan.crop_name.ilike(f"%{crop}%"))

    if healthy is not None:
        is_healthy = healthy.lower() == "true"
        query = query.filter_by(is_healthy=is_healthy)

    if severity:
        query = query.filter_by(severity=severity)

    query      = query.order_by(Scan.scanned_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "scans":       [s.to_dict() for s in pagination.items],
        "total":       pagination.total,
        "page":        page,
        "per_page":    per_page,
        "pages":       pagination.pages,
        "has_next":    pagination.has_next,
        "has_prev":    pagination.has_prev,
    }), 200


# ── GET /api/history/<id> ───────────────────────────────────
@history_bp.route("/history/<int:scan_id>", methods=["GET"])
@jwt_required()
def get_scan(scan_id):
    user_id = int(get_jwt_identity())
    scan    = Scan.query.filter_by(id=scan_id, user_id=user_id).first()

    if not scan:
        return jsonify({"error": "Scan not found"}), 404

    return jsonify({"scan": scan.to_dict()}), 200


# ── DELETE /api/history/<id> ────────────────────────────────
@history_bp.route("/history/<int:scan_id>", methods=["DELETE"])
@jwt_required()
def delete_scan(scan_id):
    user_id = int(get_jwt_identity())
    scan    = Scan.query.filter_by(id=scan_id, user_id=user_id).first()

    if not scan:
        return jsonify({"error": "Scan not found"}), 404

    import os
    from flask import current_app
    image_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"], scan.image_filename
    )
    if os.path.exists(image_path):
        os.remove(image_path)

    db.session.delete(scan)
    db.session.commit()

    return jsonify({"message": "Scan deleted successfully"}), 200


# ── GET /api/history/stats ──────────────────────────────────
@history_bp.route("/history/stats", methods=["GET"])
@jwt_required()
def get_stats():
    """
    Aggregate scan statistics for the dashboard.
    Returns totals, disease breakdown, crop breakdown,
    weekly trend and severity distribution.
    """
    user_id = int(get_jwt_identity())

    total    = Scan.query.filter_by(user_id=user_id).count()
    healthy  = Scan.query.filter_by(user_id=user_id, is_healthy=True).count()
    diseased = total - healthy

    # Top diseases
    top_diseases = (
        db.session.query(Scan.disease_name, func.count(Scan.id).label("count"))
        .filter_by(user_id=user_id, is_healthy=False)
        .group_by(Scan.disease_name)
        .order_by(func.count(Scan.id).desc())
        .limit(5)
        .all()
    )

    # Crop breakdown
    crop_breakdown = (
        db.session.query(Scan.crop_name, func.count(Scan.id).label("count"))
        .filter_by(user_id=user_id)
        .group_by(Scan.crop_name)
        .order_by(func.count(Scan.id).desc())
        .all()
    )

    # Severity distribution
    severity_dist = (
        db.session.query(Scan.severity, func.count(Scan.id).label("count"))
        .filter_by(user_id=user_id)
        .group_by(Scan.severity)
        .all()
    )

    # Weekly trend — last 7 days
    from datetime import datetime, timedelta
    weekly = []
    for i in range(6, -1, -1):
        day   = datetime.utcnow() - timedelta(days=i)
        start = day.replace(hour=0,  minute=0,  second=0,  microsecond=0)
        end   = day.replace(hour=23, minute=59, second=59, microsecond=999999)
        count = (
            Scan.query
            .filter_by(user_id=user_id)
            .filter(Scan.scanned_at >= start, Scan.scanned_at <= end)
            .count()
        )
        weekly.append({"date": day.strftime("%a"), "scans": count})

    # Average confidence
    avg_conf = (
        db.session.query(func.avg(Scan.confidence))
        .filter_by(user_id=user_id)
        .scalar()
    )

    return jsonify({
        "total":            total,
        "healthy":          healthy,
        "diseased":         diseased,
        "health_rate":      round((healthy / total * 100), 1) if total > 0 else 0,
        "avg_confidence":   round(float(avg_conf or 0) * 100, 1),
        "top_diseases":     [{"name": d, "count": c} for d, c in top_diseases],
        "crop_breakdown":   [{"crop": c, "count": n} for c, n in crop_breakdown],
        "severity_dist":    [{"severity": s, "count": c} for s, c in severity_dist],
        "weekly_trend":     weekly,
    }), 200
