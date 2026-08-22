# This script reduces our merged 21-class dataset down to a manageable
# subset for faster CPU training: max 300 images per class in the
# training set. Valid/test sets are left as-is since they're already
# much smaller and don't need reduction.
#
# Since one image can contain multiple classes (multi-object detection),
# we count "images per class" by scanning each label file's class IDs,
# and keep an image as long as at least one of its classes still needs
# more examples.

import os
import random
from collections import defaultdict

TRAIN_DIR = "/app/training_data/train"
MAX_PER_CLASS = 300

random.seed(42)  # reproducible selection

images_dir = os.path.join(TRAIN_DIR, "images")
labels_dir = os.path.join(TRAIN_DIR, "labels")

all_images = os.listdir(images_dir)
random.shuffle(all_images)  # shuffle so we don't just take the first N alphabetically

class_counts = defaultdict(int)
keep_images = []
remove_images = []

for filename in all_images:
    label_filename = os.path.splitext(filename)[0] + ".txt"
    label_path = os.path.join(labels_dir, label_filename)

    if not os.path.exists(label_path):
        remove_images.append(filename)
        continue

    with open(label_path, "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    classes_in_image = set(int(l.split()[0]) for l in lines)

    # Keep this image if ANY of its classes still needs more examples
    needs_more = any(class_counts[c] < MAX_PER_CLASS for c in classes_in_image)

    if needs_more:
        keep_images.append(filename)
        for c in classes_in_image:
            class_counts[c] += 1
    else:
        remove_images.append(filename)

print(f"Keeping {len(keep_images)} images, removing {len(remove_images)} images")
print("Final counts per class:")
for class_id in sorted(class_counts.keys()):
    print(f"  class {class_id}: {class_counts[class_id]} images")

# Actually delete the excess images + labels
for filename in remove_images:
    img_path = os.path.join(images_dir, filename)
    label_path = os.path.join(labels_dir, os.path.splitext(filename)[0] + ".txt")

    if os.path.exists(img_path):
        os.remove(img_path)
    if os.path.exists(label_path):
        os.remove(label_path)

print("\nDone subsampling training set.")