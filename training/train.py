
# ============================================================
#  PhytoSense — CNN Training Script
#  training/train.py
#
#  Usage:
#    python train.py --data_dir ./dataset --epochs 50
# ============================================================

import os
import json
import argparse
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import (
    EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
)


# ── Argument parser ─────────────────────────────────────────
parser = argparse.ArgumentParser(description="Train PhytoSense CNN")
parser.add_argument("--data_dir",   default="./dataset",      help="Path to PlantVillage dataset")
parser.add_argument("--model_out",  default="../model/plant_cnn.h5", help="Output model path")
parser.add_argument("--epochs",     default=50,  type=int)
parser.add_argument("--batch_size", default=32,  type=int)
parser.add_argument("--img_size",   default=224, type=int)
parser.add_argument("--lr",         default=0.001, type=float)
args = parser.parse_args()

IMG_SIZE   = (args.img_size, args.img_size)
BATCH_SIZE = args.batch_size
EPOCHS     = args.epochs
DATA_DIR   = args.data_dir
MODEL_OUT  = args.model_out

print("=" * 55)
print("  PhytoSense CNN — Training")
print(f"  Dataset : {DATA_DIR}")
print(f"  Epochs  : {EPOCHS}")
print(f"  Batch   : {BATCH_SIZE}")
print(f"  ImgSize : {IMG_SIZE}")
print("=" * 55)


# ── Load dataset ────────────────────────────────────────────
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split = 0.15,
    subset           = "training",
    seed             = 42,
    image_size       = IMG_SIZE,
    batch_size       = BATCH_SIZE,
    label_mode       = "int",
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split = 0.15,
    subset           = "validation",
    seed             = 42,
    image_size       = IMG_SIZE,
    batch_size       = BATCH_SIZE,
    label_mode       = "int",
)

class_names = train_ds.class_names
num_classes = len(class_names)
print(f"\n[PhytoSense] Classes found: {num_classes}")
print(f"[PhytoSense] Classes: {class_names}\n")

# Save class names
os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
class_names_path = os.path.join(os.path.dirname(MODEL_OUT), "class_names.json")
with open(class_names_path, "w") as f:
    json.dump(class_names, f, indent=2)
print(f"[PhytoSense] Class names saved to {class_names_path}")

# ── Class weights for imbalanced dataset ────────────────────
total_samples = sum(1 for _ in train_ds.unbatch())
class_counts  = {}
for _, labels in train_ds.unbatch():
    label = int(labels.numpy())
    class_counts[label] = class_counts.get(label, 0) + 1

class_weights = {
    cls: total_samples / (num_classes * count)
    for cls, count in class_counts.items()
}

# ── Performance optimisation ────────────────────────────────
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds   = val_ds.cache().prefetch(buffer_size=AUTOTUNE)


# ── Model architecture ──────────────────────────────────────
def build_phytosense_cnn(num_classes: int, img_size: tuple) -> keras.Model:
    """
    PhytoSense 9-layer CNN as described in the conference paper.
    3 convolutional blocks + classifier head.
    Total params: ~372,678
    """
    inputs = keras.Input(shape=(*img_size, 3))

    # Augmentation layer
    x = layers.RandomFlip("horizontal_and_vertical")(inputs)
    x = layers.RandomRotation(0.2)(x)
    x = layers.RandomZoom(0.15)(x)
    x = layers.RandomTranslation(0.1, 0.1)(x)
    x = layers.RandomBrightness(0.1)(x)

    # Normalisation
    x = layers.Rescaling(1.0 / 255)(x)

    # Block 1 — 32 filters
    x = layers.Conv2D(32, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.Conv2D(32, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Dropout(0.25)(x)

    # Block 2 — 64 filters
    x = layers.Conv2D(64, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.Conv2D(64, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Dropout(0.25)(x)

    # Block 3 — 128 filters
    x = layers.Conv2D(128, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.Conv2D(128, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Dropout(0.30)(x)

    # Classifier head
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(512, activation="relu")(x)
    x = layers.Dropout(0.50)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    return keras.Model(inputs, outputs, name="PhytoSense_CNN")


model = build_phytosense_cnn(num_classes, IMG_SIZE)
model.summary()

# ── Compile ─────────────────────────────────────────────────
model.compile(
    optimizer = keras.optimizers.Adam(learning_rate=args.lr),
    loss      = "sparse_categorical_crossentropy",
    metrics   = ["accuracy", keras.metrics.SparseTopKCategoricalAccuracy(k=3, name="top3_acc")],
)

# ── Callbacks ────────────────────────────────────────────────
callbacks = [
    EarlyStopping(
        monitor              = "val_accuracy",
        patience             = 8,
        restore_best_weights = True,
        verbose              = 1,
    ),
    ReduceLROnPlateau(
        monitor  = "val_accuracy",
        factor   = 0.5,
        patience = 4,
        min_lr   = 1e-6,
        verbose  = 1,
    ),
    ModelCheckpoint(
        filepath          = MODEL_OUT,
        monitor           = "val_accuracy",
        save_best_only    = True,
        save_weights_only = False,
        verbose           = 1,
    ),
]

# ── Train ────────────────────────────────────────────────────
print("\n[PhytoSense] Starting training...\n")
history = model.fit(
    train_ds,
    validation_data = val_ds,
    epochs          = EPOCHS,
    callbacks       = callbacks,
    class_weight    = class_weights,
    verbose         = 1,
)

# ── Save final results ───────────────────────────────────────
final_acc     = max(history.history["val_accuracy"])
final_top3    = max(history.history["val_top3_acc"])
total_epochs  = len(history.history["val_accuracy"])

print("\n" + "=" * 55)
print("  PhytoSense CNN — Training Complete")
print(f"  Best Val Accuracy : {final_acc*100:.2f}%")
print(f"  Best Val Top-3    : {final_top3*100:.2f}%")
print(f"  Epochs trained    : {total_epochs}")
print(f"  Model saved to    : {MODEL_OUT}")
print("=" * 55)
