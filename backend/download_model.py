import os
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "plant_cnn_fixed.keras")
if os.path.exists(MODEL_PATH):
    print(f"Model already exists: {os.path.getsize(MODEL_PATH)} bytes")
else:
    print("Model not found!")
