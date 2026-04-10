
# ============================================================
#  PhytoSense — Authentication Routes
#  backend/routes/auth.py
# ============================================================

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from models.db import db
from models.user import User
from models.farm import Farm

auth_bp = Blueprint("auth", __name__)


# ── POST /api/auth/register ─────────────────────────────────
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    # Validate required fields
    required = ["email", "password", "full_name"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    email    = data["email"].strip().lower()
    password = data["password"]
    name     = data["full_name"].strip()

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists"}), 409

    # Create user
    user = User(email=email, full_name=name, phone=data.get("phone"))
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    # Create default farm profile
    farm = Farm(
        user_id      = user.id,
        farm_name    = data.get("farm_name", f"{name}'s Farm"),
        primary_crop = data.get("primary_crop", "Tomato"),
        soil_type    = data.get("soil_type", "Clay Loam"),
        location_str = data.get("location", "India"),
        latitude     = data.get("latitude", 26.8467),
        longitude    = data.get("longitude", 80.9462),
        area_hectares= data.get("area_hectares", 1.0),
    )
    db.session.add(farm)
    db.session.commit()

    access_token  = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "message":       "Account created successfully",
        "access_token":  access_token,
        "refresh_token": refresh_token,
        "user":          user.to_dict(),
    }), 201


# ── POST /api/auth/login ────────────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email    = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.is_active:
        return jsonify({"error": "Account is deactivated"}), 403

    access_token  = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        "message":       "Login successful",
        "access_token":  access_token,
        "refresh_token": refresh_token,
        "user":          user.to_dict(),
    }), 200


# ── POST /api/auth/refresh ──────────────────────────────────
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity     = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token": access_token}), 200


# ── GET /api/auth/me ────────────────────────────────────────
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user    = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": user.to_dict()}), 200
