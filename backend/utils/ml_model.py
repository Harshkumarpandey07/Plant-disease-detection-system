
# ============================================================
#  PhytoSense — ML Model Loader & Inference Engine
#  backend/utils/ml_model.py
# ============================================================

import os
import json
import random
import numpy as np
from PIL import Image

# ── Default 38 PlantVillage class names ────────────────────
DEFAULT_CLASSES = [
    "Apple — Apple Scab",
    "Apple — Black Rot",
    "Apple — Cedar Apple Rust",
    "Apple — Healthy",
    "Blueberry — Healthy",
    "Cherry — Powdery Mildew",
    "Cherry — Healthy",
    "Corn — Cercospora Leaf Spot",
    "Corn — Common Rust",
    "Corn — Northern Leaf Blight",
    "Corn — Healthy",
    "Grape — Black Rot",
    "Grape — Esca Black Measles",
    "Grape — Leaf Blight",
    "Grape — Healthy",
    "Orange — Citrus Greening",
    "Peach — Bacterial Spot",
    "Peach — Healthy",
    "Pepper — Bacterial Spot",
    "Pepper — Healthy",
    "Potato — Early Blight",
    "Potato — Late Blight",
    "Potato — Healthy",
    "Raspberry — Healthy",
    "Soybean — Healthy",
    "Squash — Powdery Mildew",
    "Strawberry — Leaf Scorch",
    "Strawberry — Healthy",
    "Tomato — Bacterial Spot",
    "Tomato — Early Blight",
    "Tomato — Late Blight",
    "Tomato — Leaf Mold",
    "Tomato — Septoria Leaf Spot",
    "Tomato — Spider Mites",
    "Tomato — Target Spot",
    "Tomato — Yellow Leaf Curl Virus",
    "Tomato — Mosaic Virus",
    "Tomato — Healthy",
]

# ── Module-level model cache ────────────────────────────────
_model       = None
_class_names = None
_mock_mode   = False


def _load_model(model_path: str, class_names_path: str):
    """Lazy-load the TensorFlow model. Falls back to mock mode."""
    global _model, _class_names, _mock_mode

    if _model is not None:
        return

    # Load class names
    if os.path.exists(class_names_path):
        with open(class_names_path, "r") as f:
            _class_names = json.load(f)
    else:
        _class_names = DEFAULT_CLASSES

    # Load model
    if os.path.exists(model_path):
        try:
            import tensorflow as tf
            _model     = tf.keras.models.load_model(model_path)
            _mock_mode = False
            print(f"[PhytoSense ML] Model loaded: {model_path}")
            print(f"[PhytoSense ML] Classes: {len(_class_names)}")
        except Exception as e:
            print(f"[PhytoSense ML] Model load failed: {e}")
            _mock_mode = True
    else:
        print(f"[PhytoSense ML] Model not found at {model_path} — using mock mode")
        _mock_mode = True


def _preprocess_image(image_path: str, img_size: tuple) -> "np.ndarray":
    """Load and preprocess image for CNN inference."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize(img_size, Image.LANCZOS)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def _mock_predict(image_path: str) -> dict:
    """
    Deterministic mock prediction for development and testing.
    Uses image filename hash as seed so same image always
    returns the same prediction.
    """
    seed = sum(ord(c) for c in os.path.basename(image_path))
    rng  = random.Random(seed)

    # Pick a disease class
    idx          = rng.randint(0, len(DEFAULT_CLASSES) - 1)
    disease_name = DEFAULT_CLASSES[idx]
    confidence   = round(rng.uniform(0.72, 0.98), 4)
    is_healthy   = "Healthy" in disease_name

    # Build top-3 predictions
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
        top3.append({
            "disease":    DEFAULT_CLASSES[class_idx],
            "confidence": conf,
        })

    # Severity
    if is_healthy:
        severity = "healthy"
    elif confidence > 0.85:
        severity = "high"
    elif confidence > 0.65:
        severity = "medium"
    else:
        severity = "low"

    crop = disease_name.split(" — ")[0] if " — " in disease_name else "Unknown"

    return {
        "disease_name": disease_name,
        "crop_name":    crop,
        "confidence":   confidence,
        "is_healthy":   is_healthy,
        "severity":     severity,
        "top3":         top3,
        "mock_mode":    True,
    }


def predict(
    image_path:      str,
    model_path:      str,
    class_names_path: str,
    img_size:        tuple = (224, 224),
) -> dict:
    """
    Run inference on a plant leaf image.
    Returns disease name, crop, confidence, severity and top-3.
    Falls back to deterministic mock if model is unavailable.
    """
    _load_model(model_path, class_names_path)

    if _mock_mode:
        return _mock_predict(image_path)

    try:
        img_array = _preprocess_image(image_path, img_size)
        preds     = _model.predict(img_array, verbose=0)[0]

        # Top-3 predictions
        top3_idx  = np.argsort(preds)[::-1][:3]
        top3      = [
            {
                "disease":    _class_names[i],
                "confidence": float(round(preds[i], 4)),
            }
            for i in top3_idx
        ]

        best_idx     = int(top3_idx[0])
        disease_name = _class_names[best_idx]
        confidence   = float(round(preds[best_idx], 4))
        is_healthy   = "Healthy" in disease_name

        # Severity classification
        if is_healthy:
            severity = "healthy"
        elif confidence > 0.85:
            severity = "high"
        elif confidence > 0.65:
            severity = "medium"
        else:
            severity = "low"

        crop = disease_name.split(" — ")[0] if " — " in disease_name else "Unknown"

        return {
            "disease_name": disease_name,
            "crop_name":    crop,
            "confidence":   confidence,
            "is_healthy":   is_healthy,
            "severity":     severity,
            "top3":         top3,
            "mock_mode":    False,
        }

    except Exception as e:
        print(f"[PhytoSense ML] Inference error: {e}")
        return _mock_predict(image_path)
