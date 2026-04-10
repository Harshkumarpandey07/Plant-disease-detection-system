
# ============================================================
#  PhytoSense — Model Evaluation Script
#  training/evaluate.py
#
#  Usage:
#    python evaluate.py --data_dir ./dataset --model_path ../model/plant_cnn.h5
# ============================================================

import os
import json
import argparse
import numpy as np
import tensorflow as tf
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    top_k_accuracy_score,
)

parser = argparse.ArgumentParser(description="Evaluate PhytoSense CNN")
parser.add_argument("--data_dir",   default="./dataset",            help="Dataset path")
parser.add_argument("--model_path", default="../model/plant_cnn.h5", help="Trained model path")
parser.add_argument("--img_size",   default=224, type=int)
parser.add_argument("--batch_size", default=32,  type=int)
args = parser.parse_args()

IMG_SIZE   = (args.img_size, args.img_size)
BATCH_SIZE = args.batch_size

print("=" * 55)
print("  PhytoSense CNN — Evaluation")
print(f"  Model  : {args.model_path}")
print(f"  Data   : {args.data_dir}")
print("=" * 55)

# ── Load test dataset (held-out 15%) ────────────────────────
test_ds = tf.keras.utils.image_dataset_from_directory(
    args.data_dir,
    validation_split = 0.15,
    subset           = "validation",
    seed             = 42,
    image_size       = IMG_SIZE,
    batch_size       = BATCH_SIZE,
    label_mode       = "int",
    shuffle          = False,
)

class_names = test_ds.class_names
print(f"\n[PhytoSense] Classes: {len(class_names)}")

# ── Load model ───────────────────────────────────────────────
model = tf.keras.models.load_model(args.model_path)
print(f"[PhytoSense] Model loaded successfully\n")

# ── Get predictions ──────────────────────────────────────────
print("[PhytoSense] Running inference on test set...")
y_true = []
y_pred_probs = []

for images, labels in test_ds:
    preds = model.predict(images, verbose=0)
    y_pred_probs.extend(preds)
    y_true.extend(labels.numpy())

y_true       = np.array(y_true)
y_pred_probs = np.array(y_pred_probs)
y_pred       = np.argmax(y_pred_probs, axis=1)

# ── Metrics ──────────────────────────────────────────────────
top1_acc = accuracy_score(y_true, y_pred)
top3_acc = top_k_accuracy_score(y_true, y_pred_probs, k=3)
top5_acc = top_k_accuracy_score(y_true, y_pred_probs, k=5)

print("\n" + "=" * 55)
print("  PHYTOSENSE CNN — EVALUATION RESULTS")
print("=" * 55)
print(f"  Top-1 Accuracy : {top1_acc*100:.2f}%")
print(f"  Top-3 Accuracy : {top3_acc*100:.2f}%")
print(f"  Top-5 Accuracy : {top5_acc*100:.2f}%")
print("=" * 55)

# ── Per-class report ─────────────────────────────────────────
print("\nPer-Class Classification Report:")
print("-" * 55)
report = classification_report(
    y_true, y_pred,
    target_names = class_names,
    digits       = 4,
)
print(report)

# ── Save results ─────────────────────────────────────────────
results = {
    "top1_accuracy": round(top1_acc, 4),
    "top3_accuracy": round(top3_acc, 4),
    "top5_accuracy": round(top5_acc, 4),
    "num_classes":   len(class_names),
    "class_names":   class_names,
}

out_path = os.path.join(os.path.dirname(args.model_path), "eval_results.json")
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n[PhytoSense] Results saved to {out_path}")
print("\n[PhytoSense] Evaluation complete.")
