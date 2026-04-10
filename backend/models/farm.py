
# ============================================================
#  PhytoSense — Farm & Scan Models
#  backend/models/farm.py
# ============================================================

from datetime import datetime
import json
from models.db import db


class Farm(db.Model):
    __tablename__ = "farms"

    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # ── Location ───────────────────────────────────────────
    farm_name     = db.Column(db.String(100), default="My Farm")
    latitude      = db.Column(db.Float,       default=26.8467)
    longitude     = db.Column(db.Float,       default=80.9462)
    location_str  = db.Column(db.String(200), default="Lucknow, UP, India")

    # ── Farm Details ───────────────────────────────────────
    area_hectares = db.Column(db.Float,      default=1.0)
    primary_crop  = db.Column(db.String(50), default="Tomato")
    soil_type     = db.Column(db.String(50), default="Clay Loam")
    growth_stage  = db.Column(db.String(50), default="Vegetative")

    # ── Notification Preferences ───────────────────────────
    notify_disease    = db.Column(db.Boolean, default=True)
    notify_irrigation = db.Column(db.Boolean, default=True)
    notify_weather    = db.Column(db.Boolean, default=True)
    notify_weekly     = db.Column(db.Boolean, default=True)

    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "farm_name":          self.farm_name,
            "latitude":           self.latitude,
            "longitude":          self.longitude,
            "location_str":       self.location_str,
            "area_hectares":      self.area_hectares,
            "primary_crop":       self.primary_crop,
            "soil_type":          self.soil_type,
            "growth_stage":       self.growth_stage,
            "notify_disease":     self.notify_disease,
            "notify_irrigation":  self.notify_irrigation,
            "notify_weather":     self.notify_weather,
            "notify_weekly":      self.notify_weekly,
        }


# ============================================================
#  Scan Model — one record per disease detection
# ============================================================

class Scan(db.Model):
    __tablename__ = "scans"

    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # ── Image ──────────────────────────────────────────────
    image_filename = db.Column(db.String(260), nullable=False)
    source         = db.Column(db.String(20),  default="upload")  # upload | camera

    # ── Prediction ─────────────────────────────────────────
    disease_name   = db.Column(db.String(100), nullable=False)
    crop_name      = db.Column(db.String(60),  nullable=False)
    confidence     = db.Column(db.Float,       nullable=False)
    is_healthy     = db.Column(db.Boolean,     default=False)
    severity       = db.Column(db.String(20),  default="medium")  # low|medium|high|healthy
    top3_json      = db.Column(db.Text,        default="[]")

    # ── Weather Context at Scan Time ───────────────────────
    temperature    = db.Column(db.Float,      nullable=True)
    humidity       = db.Column(db.Float,      nullable=True)
    weather_desc   = db.Column(db.String(80), nullable=True)

    # ── Location ───────────────────────────────────────────
    latitude       = db.Column(db.Float, nullable=True)
    longitude      = db.Column(db.Float, nullable=True)

    scanned_at     = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self) -> dict:
        return {
            "id":           self.id,
            "image_url":    f"/static/uploads/{self.image_filename}",
            "source":       self.source,
            "disease_name": self.disease_name,
            "crop_name":    self.crop_name,
            "confidence":   round(self.confidence, 4),
            "is_healthy":   self.is_healthy,
            "severity":     self.severity,
            "top3":         json.loads(self.top3_json),
            "weather": {
                "temperature": self.temperature,
                "humidity":    self.humidity,
                "description": self.weather_desc,
            },
            "location": {
                "lat": self.latitude,
                "lon": self.longitude,
            },
            "scanned_at": self.scanned_at.isoformat(),
        }
