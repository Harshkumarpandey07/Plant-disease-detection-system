# ============================================================
#  PhytoSense — ML Model Loader & Inference Engine
#  backend/utils/ml_model.py
# ============================================================
import os
import json
import random
import numpy as np
from PIL import Image

DEFAULT_CLASSES = [
    "Apple — Apple Scab", "Apple — Black Rot", "Apple — Cedar Apple Rust",
    "Apple — Healthy", "Blueberry — Healthy", "Cherry — Powdery Mildew",
    "Cherry — Healthy", "Corn — Cercospora Leaf Spot", "Corn — Common Rust",
    "Corn — Northern Leaf Blight", "Corn — Healthy", "Grape — Black Rot",
    "Grape — Esca Black Measles", "Grape — Leaf Blight", "Grape — Healthy",
    "Orange — Citrus Greening", "Peach — Bacterial Spot", "Peach — Healthy",
    "Pepper — Bacterial Spot", "Pepper — Healthy", "Potato — Early Blight",
    "Potato — Late Blight", "Potato — Healthy", "Raspberry — Healthy",
    "Soybean — Healthy", "Squash — Powdery Mildew", "Strawberry — Leaf Scorch",
    "Strawberry — Healthy", "Tomato — Bacterial Spot", "Tomato — Early Blight",
    "Tomato — Late Blight", "Tomato — Leaf Mold", "Tomato — Septoria Leaf Spot",
    "Tomato — Spider Mites", "Tomato — Target Spot",
    "Tomato — Yellow Leaf Curl Virus", "Tomato — Mosaic Virus", "Tomato — Healthy",
]

_model       = None
_class_names = None
_mock_mode   = False

def _load_model(model_path: str, class_names_path: str):
    global _model, _class_names, _mock_mode
    if _model is not None:
        return
    if os.path.exists(class_names_path):
        with open(class_names_path, "r") as f:
            raw = json.load(f)
            # Convert PlantVillage format to readable format
            _class_names = []
            for name in raw:
                parts = name.replace("___", "|").replace("_", " ").split("|")
                if len(parts) == 2:
                    crop = parts[0].strip()
                    disease = parts[1].strip()
                    if disease.lower() == "healthy":
                        _class_names.append(f"{crop} — Healthy")
                    else:
                        _class_names.append(f"{crop} — {disease}")
                else:
                    _class_names.append(name.replace("_", " "))
    else:
        _class_names = DEFAULT_CLASSES

    if os.path.exists(model_path):
        try:
            import tensorflow as tf
            _model     = tf.keras.models.load_model(model_path)
            _mock_mode = False
            print(f"[PhytoSense ML] ✅ Model loaded: {model_path}")
            print(f"[PhytoSense ML] ✅ Classes: {len(_class_names)}")
        except Exception as e:
            print(f"[PhytoSense ML] Model load failed: {e}")
            _mock_mode = True
    else:
        print(f"[PhytoSense ML] Model not found at {model_path} — using mock mode")
        _mock_mode = True

def _preprocess_image(image_path: str, img_size: tuple) -> "np.ndarray":
    """Load and preprocess image for MobileNetV2 inference."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize(img_size, Image.LANCZOS)
    arr = np.array(img, dtype=np.float32)
    # MobileNetV2 requires [-1, 1] range
    arr = (arr / 127.5) - 1.0
    return np.expand_dims(arr, axis=0)

def _mock_predict(image_path: str) -> dict:
    seed = sum(ord(c) for c in os.path.basename(image_path))
    rng  = random.Random(seed)
    idx          = rng.randint(0, len(DEFAULT_CLASSES) - 1)
    disease_name = DEFAULT_CLASSES[idx]
    confidence   = round(rng.uniform(0.72, 0.98), 4)
    is_healthy   = "Healthy" in disease_name
    indices = [idx]
    while len(indices) < 3:
        alt = rng.randint(0, len(DEFAULT_CLASSES) - 1)
        if alt not in indices:
            indices.append(alt)
    top3 = []
    remaining = 1.0
    for i, class_idx in enumerate(indices):
        if i == 0:
            conf = confidence
        elif i == 1:
            conf = round(remaining * rng.uniform(0.4, 0.7), 4)
        else:
            conf = round(remaining - top3[1]["confidence"], 4)
        remaining -= conf
        top3.append({"disease": DEFAULT_CLASSES[class_idx], "confidence": conf})
    severity = "healthy" if is_healthy else ("high" if confidence > 0.85 else ("medium" if confidence > 0.65 else "low"))
    crop = disease_name.split(" — ")[0] if " — " in disease_name else "Unknown"
    return {
        "disease_name": disease_name, "crop_name": crop,
        "confidence": confidence, "is_healthy": is_healthy,
        "severity": severity, "top3": top3, "mock_mode": True,
    }

def predict(
    image_path: str, model_path: str,
    class_names_path: str, img_size: tuple = (224, 224),
) -> dict:
    _load_model(model_path, class_names_path)
    if _mock_mode:
        return _mock_predict(image_path)
    try:
        img_array = _preprocess_image(image_path, img_size)
        preds     = _model.predict(img_array, verbose=0)[0]
        top3_idx  = np.argsort(preds)[::-1][:3]
        top3      = [
            {"disease": _class_names[i], "confidence": float(round(preds[i], 4))}
            for i in top3_idx
        ]
        best_idx     = int(top3_idx[0])
        disease_name = _class_names[best_idx]
        confidence   = float(round(preds[best_idx], 4))
        is_healthy   = "Healthy" in disease_name
        severity = "healthy" if is_healthy else ("high" if confidence > 0.85 else ("medium" if confidence > 0.65 else "low"))
        crop = disease_name.split(" — ")[0] if " — " in disease_name else "Unknown"
        return {
            "disease_name": disease_name, "crop_name": crop,
            "confidence": confidence, "is_healthy": is_healthy,
            "severity": severity, "top3": top3, "mock_mode": False,
        }
    except Exception as e:
        print(f"[PhytoSense ML] Inference error: {e}")
        return _mock_predict(image_path)
