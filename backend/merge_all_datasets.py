# This script merges THREE dataset sources into one unified training_data folder:
#
# 1. Our original 4-class dataset (chapati, dal makhni, fried rice, kadai paneer)
#    - already sits in training_data/ as classes 0-3, left untouched
#
# 2. Chicken-Biryani dataset (1 class: Chicken-Biryani) -> becomes class 4
#
# 3. Indian food detection dataset (17 classes) -> becomes classes 4-20,
#    with its "Biryani" class MERGED into the same class 4 as Chicken-Biryani
#    (both represent the same food, just from different sources)
#
# This script is designed to run INSIDE the Docker container, where all
# paths are relative to /app (the container's working directory, which
# mirrors your local backend/ folder via the volume mount).

import os
import shutil

DEST_DIR = "/app/training_data"
SPLITS = ["train", "valid", "test"]

# ------------------------------------------------------------------
# Unified class list (order matters - this defines the final IDs)
# ------------------------------------------------------------------
UNIFIED_CLASSES = [
    "chapati", "dal makhni", "fried rice", "kadai paneer",   # 0-3 (existing)
    "biryani",                                                  # 4
    "Bhatura", "BhindiMasala", "Chole", "ShahiPaneer",
    "chicken", "dal", "dhokla", "gulab_jamun", "idli",
    "jalebi", "modak", "palak_paneer", "poha", "rice",
    "roti", "samosa",                                           # 5-20
]

CLASS_TO_ID = {name: i for i, name in enumerate(UNIFIED_CLASSES)}


def relabel_and_copy(src_dir: str, split: str, prefix: str, old_class_names: list, class_name_map: dict = None):
    """
    Copies images+labels from a source dataset split into our unified
    training_data folder, remapping class IDs along the way.
    """
    src_images = os.path.join(src_dir, split, "images")
    src_labels = os.path.join(src_dir, split, "labels")
    dst_images = os.path.join(DEST_DIR, split, "images")
    dst_labels = os.path.join(DEST_DIR, split, "labels")

    os.makedirs(dst_images, exist_ok=True)
    os.makedirs(dst_labels, exist_ok=True)

    if not os.path.exists(src_images):
        print(f"  (no {split} folder in this source, skipping)")
        return 0

    count = 0
    for filename in os.listdir(src_images):
        new_image_name = f"{prefix}_{filename}"
        shutil.copy(
            os.path.join(src_images, filename),
            os.path.join(dst_images, new_image_name),
        )

        label_filename = os.path.splitext(filename)[0] + ".txt"
        src_label_path = os.path.join(src_labels, label_filename)

        if os.path.exists(src_label_path):
            new_label_name = f"{prefix}_{label_filename}"
            dst_label_path = os.path.join(dst_labels, new_label_name)

            with open(src_label_path, "r") as f_in:
                lines = f_in.readlines()

            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if not parts:
                    continue

                old_id = int(parts[0])
                old_name = old_class_names[old_id]

                if class_name_map and old_name in class_name_map:
                    old_name = class_name_map[old_name]

                new_id = CLASS_TO_ID[old_name]
                parts[0] = str(new_id)
                new_lines.append(" ".join(parts))

            with open(dst_label_path, "w") as f_out:
                f_out.write("\n".join(new_lines) + "\n")

        count += 1

    return count


# ------------------------------------------------------------------
# Source 1: Chicken-Biryani dataset
# ------------------------------------------------------------------
print("Merging Chicken-Biryani dataset...")
biryani_classes = ["Chicken-Biryani"]
biryani_rename = {"Chicken-Biryani": "biryani"}

for split in SPLITS:
    n = relabel_and_copy(
        "/app/biryani-dataset", split, "cb",
        biryani_classes, biryani_rename,
    )
    print(f"  {split}: {n} images")

# ------------------------------------------------------------------
# Source 2: Indian food detection dataset (17 classes)
# ------------------------------------------------------------------
print("\nMerging Indian food detection dataset (17 classes)...")
ifd_classes = [
    "Bhatura", "BhindiMasala", "Biryani", "Chole", "ShahiPaneer",
    "chicken", "dal", "dhokla", "gulab_jamun", "idli", "jalebi",
    "modak", "palak_paneer", "poha", "rice", "roti", "samosa",
]
ifd_rename = {"Biryani": "biryani"}

for split in SPLITS:
    n = relabel_and_copy(
        "/app/indian-food-detection-v2", split, "ifd",
        ifd_classes, ifd_rename,
    )
    print(f"  {split}: {n} images")

# ------------------------------------------------------------------
# Write the updated data.yaml with all 21 classes
# ------------------------------------------------------------------
yaml_content = f"""path: /app/training_data
train: train/images
val: valid/images
test: test/images

nc: {len(UNIFIED_CLASSES)}
names: {UNIFIED_CLASSES}
"""

with open(os.path.join(DEST_DIR, "data.yaml"), "w") as f:
    f.write(yaml_content)

print(f"\nDone. Unified dataset now has {len(UNIFIED_CLASSES)} classes.")
print("Updated data.yaml written.")