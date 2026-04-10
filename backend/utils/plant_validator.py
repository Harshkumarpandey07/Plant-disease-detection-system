import numpy as np
from PIL import Image
import re

PLANT_KEYWORDS = {
    'daisy', 'dandelion', 'sunflower', 'rose', 'tulip', 'orchid', 'lily',
    'mushroom', 'fungus', 'corn', 'artichoke', 'cabbage', 'broccoli',
    'cauliflower', 'zucchini', 'squash', 'cucumber', 'pepper', 'cardoon',
    'rapeseed', 'stinkhorn', 'earthstar', 'hen', 'gyromitra', 'agaric',
    'bolete', 'lemon', 'orange', 'fig', 'pineapple', 'banana', 'jackfruit',
    'pomegranate', 'strawberry', 'grape', 'pot', 'leaf', 'plant',
    'tree', 'fern', 'moss', 'lichen', 'seaweed', 'blossom', 'herb',
    'shrub', 'bush', 'vine', 'gourd', 'acorn', 'buckeye', 'hip', 'ear',
    'frond', 'petal', 'flower', 'vegetable', 'fruit', 'crop', 'garden',
    'green', 'grass', 'weed', 'tobacco', 'potato', 'tomato', 'apple',
    'peach', 'cherry', 'raspberry', 'soybean', 'wheat', 'rice',
    'taro', 'yam', 'cassava', 'eggplant', 'okra', 'spinach',
    'lettuce', 'kale', 'beet', 'radish', 'turnip', 'carrot',
    'peanut', 'bean', 'pea', 'lentil',
}

NON_PLANT_KEYWORDS = {
    'person', 'man', 'woman', 'boy', 'girl', 'face', 'human',
    'car', 'truck', 'bus', 'vehicle', 'motorcycle', 'bicycle',
    'dog', 'cat', 'bird', 'fish', 'animal',
    'building', 'house', 'sky', 'mountain', 'beach', 'ocean',
    'pizza', 'burger', 'sandwich', 'cake', 'bread',
    'phone', 'laptop', 'computer', 'keyboard',
    'chair', 'table', 'sofa', 'bed',
    'road', 'street', 'highway', 'bridge',
}

BLOCK_THRESHOLD = 0.60
PLANT_THRESHOLD = 0.05

_validator_model = None


def _get_validator():
    global _validator_model
    if _validator_model is not None:
        return _validator_model
    try:
        import keras
        print('[PhytoSense Validator] Loading MobileNetV2...')
        _validator_model = keras.applications.MobileNetV2(
            input_shape=(224, 224, 3),
            include_top=True,
            weights='imagenet',
        )
        _validator_model.trainable = False
        print('[PhytoSense Validator] ✅ Validator ready')
    except Exception as e:
        print(f'[PhytoSense Validator] Could not load: {e}')
        _validator_model = None
    return _validator_model


def is_plant_image(image_path: str) -> dict:
    model = _get_validator()

    if model is None:
        return {"is_plant": True, "confidence": 1.0, "top_label": "unknown", "message": "Validator unavailable"}

    try:
        import keras

        img = Image.open(image_path).convert('RGB').resize((224, 224), Image.LANCZOS)
        arr = np.array(img, dtype=np.float32)
        arr = (arr / 127.5) - 1.0
        arr = np.expand_dims(arr, axis=0)

        preds = model.predict(arr, verbose=0)[0]

        top10 = keras.applications.mobilenet_v2.decode_predictions(
            np.expand_dims(preds, 0), top=10
        )[0]

        top_label = top10[0][1].replace('_', ' ')
        top_conf  = float(top10[0][2])

        print(f'[Validator] Top: {[(l, round(c,3)) for _, l, c in top10[:5]]}')

        plant_conf = sum(float(c) for _, l, c in top10 if any(kw in l.lower() for kw in PLANT_KEYWORDS))
        top1_is_non_plant = (top_conf >= BLOCK_THRESHOLD and any(kw in top_label.lower() for kw in NON_PLANT_KEYWORDS))
        any_plant_in_top10 = any(any(kw in l.lower() for kw in PLANT_KEYWORDS) for _, l, _ in top10)

        is_plant = (any_plant_in_top10 or plant_conf >= PLANT_THRESHOLD) and not top1_is_non_plant

        message = (
            "Image validated as plant"
            if is_plant
            else f"This doesn't look like a plant. It looks like '{top_label}'. Please upload a clear photo of a plant leaf or crop."
        )

        return {"is_plant": is_plant, "confidence": round(plant_conf, 4), "top_label": top_label, "message": message}

    except Exception as e:
        print(f'[PhytoSense Validator] Error: {e}')
        return {"is_plant": True, "confidence": 1.0, "top_label": "unknown", "message": "Validation error"}
