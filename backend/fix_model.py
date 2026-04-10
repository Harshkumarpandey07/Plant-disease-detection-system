"""
fix_model.py - Patches plant_cnn_final.keras by removing unsupported keys
from the model config JSON inside the zip archive.
Run from: backend folder
"""
import os, sys, json, zipfile, shutil, re

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

MODEL_IN  = "model/plant_cnn_final.keras"
MODEL_OUT = "model/plant_cnn_fixed.keras"

def patch_config(obj):
    if isinstance(obj, dict):
        # Remove problematic keys
        obj.pop('quantization_config', None)
        # Fix RandomFlip data_format issue
        if obj.get('class_name') == 'RandomFlip' and 'config' in obj:
            obj['config'].pop('data_format', None)
        return {k: patch_config(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [patch_config(i) for i in obj]
    return obj

print(f"Reading {MODEL_IN} ...")
with zipfile.ZipFile(MODEL_IN, 'r') as zin:
    names = zin.namelist()
    print("Files in archive:", names)

    with zipfile.ZipFile(MODEL_OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name in names:
            data = zin.read(name)
            if name == 'config.json':
                print("Patching config.json ...")
                config = json.loads(data.decode('utf-8'))
                config = patch_config(config)
                data = json.dumps(config).encode('utf-8')
                print("config.json patched!")
            zout.writestr(name, data)

print(f"\nFixed model saved to: {MODEL_OUT}")
print("Now testing load...")

import tensorflow as tf
model = tf.keras.models.load_model(MODEL_OUT, compile=False, safe_mode=False)
print("Model loaded OK!")
print("Input shape :", model.input_shape)
print("Output shape:", model.output_shape)
