import os
import urllib.request

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "plant_cnn_full.h5")
LFS_URL = "https://media.githubusercontent.com/media/Harshkumarpandey07/Plant-disease-detection-system/main/backend/model/plant_cnn_full.h5"

os.makedirs(MODEL_DIR, exist_ok=True)

if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 1000000:
    print("Downloading model from GitHub LFS...")
    urllib.request.urlretrieve(LFS_URL, MODEL_PATH)
    print(f"Model downloaded: {os.path.getsize(MODEL_PATH)} bytes")
else:
    print(f"Model already exists: {os.path.getsize(MODEL_PATH)} bytes")