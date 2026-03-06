
# ============================================================
#  PhytoSense — Flask Application Factory
#  backend/app.py
# ============================================================

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from config import Config
from models.db import db

# ── Load environment variables ──────────────────────────────
load_dotenv()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── Ensure upload folder exists ────────────────────────
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ── Extensions ────────────────────────────────────────
    db.init_app(app)
    JWTManager(app)
    CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    # ── Register Blueprints ────────────────────────────────
    from routes.auth        import auth_bp
    from routes.predict     import predict_bp
    from routes.history     import history_bp
    from routes.weather     import weather_bp
    from routes.irrigation  import irrigation_bp
    from routes.crop_health import crop_health_bp
    from routes.disease_info import disease_bp
    from routes.user        import user_bp

    app.register_blueprint(auth_bp,        url_prefix="/api/auth")
    app.register_blueprint(predict_bp,     url_prefix="/api")
    app.register_blueprint(history_bp,     url_prefix="/api")
    app.register_blueprint(weather_bp,     url_prefix="/api")
    app.register_blueprint(irrigation_bp,  url_prefix="/api")
    app.register_blueprint(crop_health_bp, url_prefix="/api")
    app.register_blueprint(disease_bp,     url_prefix="/api")
    app.register_blueprint(user_bp,        url_prefix="/api")

    # ── Create database tables ─────────────────────────────
    with app.app_context():
        db.create_all()
        print("[PhytoSense] Database tables ready")

    # ── Health check endpoint ──────────────────────────────

    from flask import render_template


    from flask import render_template


    from flask import render_template


    from flask import render_template


    from flask import render_template

    @app.route('/')
    def serve_frontend():
        return render_template('index.html')

    return app







# ── Entry point ────────────────────────────────────────────
app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print("  PhytoSense API — Starting server")
    print("  http://127.0.0.1:5000")
    print("=" * 50)
    app.run(
        host  = "0.0.0.0",
        port  = int(os.environ.get("PORT", 5000)),
        debug = app.config["DEBUG"],
    )
