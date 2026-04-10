import os, json, random
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

_model = None
_class_names = None
_mock_mode = False


def _patch_model_file(model_path):
    """Patch the keras model file to remove unsupported config keys."""
    import zipfile
    import json as json_mod

    fixed_path = model_path.replace('.keras', '_patched.keras')
    if os.path.exists(fixed_path):
        return fixed_path

    print(f"[PhytoSense ML] Patching model file...")

    def patch_config(obj):
        if isinstance(obj, dict):
            obj.pop('quantization_config', None)
            if obj.get('class_name') == 'RandomFlip' and 'config' in obj:
                obj['config'].pop('data_format', None)
            return {k: patch_config(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [patch_config(i) for i in obj]
        return obj

    with zipfile.ZipFile(model_path, 'r') as zin:
        names = zin.namelist()
        with zipfile.ZipFile(fixed_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for name in names:
                data = zin.read(name)
                if name == 'config.json':
                    config = json_mod.loads(data.decode('utf-8'))
                    config = patch_config(config)
                    data = json_mod.dumps(config).encode('utf-8')
                zout.writestr(name, data)

    print(f"[PhytoSense ML] Model patched: {fixed_path}")
    return fixed_path


def _parse_class_name(raw):
    import re
    if "___" in raw:
        parts = raw.split("___", 1)
        crop = parts[0].strip()
        disease = parts[1].strip()
        crop = re.sub(r'\(.*?\)', '', crop).strip().strip(',').strip()
        crop = crop.replace('_', ' ').strip().title()
        disease = disease.replace('_', ' ').strip().strip(',').strip()
        if disease.lower() == 'healthy':
            disease = 'Healthy'
        else:
            disease = disease[0].upper() + disease[1:] if disease else disease
        return f"{crop} — {disease}"
    return raw.replace('_', ' ').title()


def _load_model(model_path, class_names_path):
    global _model, _class_names, _mock_mode
    if _model is not None:
        return

    # Load class names
    if os.path.exists(class_names_path):
        with open(class_names_path) as f:
            raw_names = json.load(f)
        _class_names = [_parse_class_name(n) for n in raw_names]
        print(f"[PhytoSense ML] Loaded {len(_class_names)} class names")
    else:
        _class_names = DEFAULT_CLASSES

    if os.path.exists(model_path):
        try:
            import tensorflow as tf

            # Try loading directly first
            try:
                _model = tf.keras.models.load_model(
                    model_path, compile=False, safe_mode=False
                )
                _mock_mode = False
                print(f"[PhytoSense ML] ✅ Model loaded: {model_path}")
            except Exception as e1:
                print(f"[PhytoSense ML] Direct load failed, patching: {e1}")
                patched_path = _patch_model_file(model_path)
                _model = tf.keras.models.load_model(
                    patched_path, compile=False, safe_mode=False
                )
                _mock_mode = False
                print(f"[PhytoSense ML] ✅ Model loaded (patched): {patched_path}")

            print(f"[PhytoSense ML] Classes: {len(_class_names)}")

        except Exception as e:
            print(f"[PhytoSense ML] ❌ Load failed: {e}")
            _mock_mode = True
    else:
        print(f"[PhytoSense ML] ❌ Model not found at: {model_path}")
        _mock_mode = True


def _preprocess(image_path, img_size):
    img = Image.open(image_path).convert("RGB").resize(img_size, Image.LANCZOS)
    arr = np.array(img, dtype=np.float32)
    return np.expand_dims(arr, axis=0)


def _mock_predict(image_path):
    seed = sum(ord(c) for c in os.path.basename(image_path))
    rng = random.Random(seed)
    idx = rng.randint(0, len(DEFAULT_CLASSES) - 1)
    disease_name = DEFAULT_CLASSES[idx]
    confidence = round(rng.uniform(0.72, 0.98), 4)
    is_healthy = "Healthy" in disease_name
    indices = [idx]
    while len(indices) < 3:
        alt = rng.randint(0, len(DEFAULT_CLASSES) - 1)
        if alt not in indices:
            indices.append(alt)
    top3 = []
    remaining = 1.0
    for i, ci in enumerate(indices):
        if i == 0:
            conf = confidence
        elif i == 1:
            conf = round(remaining * rng.uniform(0.4, 0.7), 4)
        else:
            conf = round(remaining - top3[1]["confidence"], 4)
        remaining -= conf
        top3.append({"disease": DEFAULT_CLASSES[ci], "confidence": conf})
    severity = "healthy" if is_healthy else ("high" if confidence > 0.85 else ("medium" if confidence > 0.65 else "low"))
    crop = disease_name.split(" — ")[0] if " — " in disease_name else "Unknown"
    return {"disease_name": disease_name, "crop_name": crop, "confidence": confidence,
            "is_healthy": is_healthy, "severity": severity, "top3": top3, "mock_mode": True}


def predict(image_path, model_path, class_names_path, img_size=(128, 128)):
    _load_model(model_path, class_names_path)
    if _mock_mode:
        print("[PhytoSense ML] ⚠️ Running in MOCK mode!")
        return _mock_predict(image_path)
    try:
        import tensorflow as tf
        arr = _preprocess(image_path, img_size)
        preds = _model.predict(arr, verbose=0)[0]
        top3_idx = np.argsort(preds)[::-1][:3]
        top3 = [{"disease": _class_names[i], "confidence": float(round(preds[i], 4))} for i in top3_idx]
        best_idx = int(top3_idx[0])
        disease_name = _class_names[best_idx]
        confidence = float(round(preds[best_idx], 4))
        is_healthy = "Healthy" in disease_name
        severity = "healthy" if is_healthy else ("high" if confidence > 0.85 else ("medium" if confidence > 0.65 else "low"))
        crop = disease_name.split(" — ")[0] if " — " in disease_name else "Unknown"
        print(f"[PhytoSense ML] ✅ Prediction: {disease_name} ({confidence:.2%})")
        return {"disease_name": disease_name, "crop_name": crop, "confidence": confidence,
                "is_healthy": is_healthy, "severity": severity, "top3": top3, "mock_mode": False}
    except Exception as e:
        print(f"[PhytoSense ML] ❌ Inference error: {e}")
        return _mock_predict(image_path)