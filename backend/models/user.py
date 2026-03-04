
# ============================================================
#  PhytoSense — User Model
#  backend/models/user.py
# ============================================================

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import db


class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer,     primary_key=True)
    email         = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name     = db.Column(db.String(100), nullable=False)
    phone         = db.Column(db.String(20),  nullable=True)
    created_at    = db.Column(db.DateTime,    default=datetime.utcnow)
    is_active     = db.Column(db.Boolean,     default=True)

    # ── Relationships ──────────────────────────────────────
    farm  = db.relationship("Farm", backref="user", uselist=False,
                            cascade="all, delete-orphan")
    scans = db.relationship("Scan", backref="user", lazy="dynamic",
                            cascade="all, delete-orphan")

    # ── Password helpers ───────────────────────────────────
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id":         self.id,
            "email":      self.email,
            "full_name":  self.full_name,
            "phone":      self.phone,
            "created_at": self.created_at.isoformat(),
            "farm":       self.farm.to_dict() if self.farm else None,
        }
