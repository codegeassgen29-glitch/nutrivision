# This script merges the downloaded Chicken-Biryani dataset into our
# existing training_data folder as a 5th class.
#
# The biryani dataset currently has its own class ID 0 (since it only
# has one class). Our merged dataset already uses:
#   0 = chapati, 1 = dal makhni, 2 = fried rice, 3 = kadai paneer
# So biryani needs to become class ID 4.
#
# Label files are plain text, one line per bounding box:
#   <class_id> <x_center> <y_center> <width> <height>
# We only need to change the first number on each line.

import os
import shutil

SOURCE_DIR = r"D:\downloads\biryani-dataset"
DEST_DIR = r"D:\nutri\nutrivision-ai\backend\training_data"
NEW_CLASS_ID = 4  # biryani becomes class 4 in the merged dataset

SPLITS = ["train", "valid", "test"]


def relabel_and_copy(split: str):
    src_images = os.path.join(SOURCE_DIR, split, "images")
    src_labels = os.path.join(SOURCE_DIR, split, "labels")
    dst_images = os.path.join(DEST_DIR, split, "images")
    dst_labels = os.path.join(DEST_DIR, split, "labels")

    os.makedirs(dst_images, exist_ok=True)
    os.makedirs(dst_labels, exist_ok=True)

    count = 0
    for filename in os.listdir(src_images):
        # Copy the image as-is, prefixing with "biryani_" to avoid
        # any filename collisions with our existing images
        new_image_name = f"biryani_{filename}"
        shutil.copy(
            os.path.join(src_images, filename),
            os.path.join(dst_images, new_image_name),
        )

        # Find the matching label file (same name, .txt extension)
        label_filename = os.path.splitext(filename)[0] + ".txt"
        src_label_path = os.path.join(src_labels, label_filename)

        if os.path.exists(src_label_path):
            new_label_name = f"biryani_{label_filename}"
            dst_label_path = os.path.join(dst_labels, new_label_name)

            with open(src_label_path, "r") as f_in:
                lines = f_in.readlines()

            # Rewrite each line, replacing the class ID (first number)
            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if not parts:
                    continue
                parts[0] = str(NEW_CLASS_ID)  # swap class ID
                new_lines.append(" ".join(parts))

            with open(dst_label_path, "w") as f_out:
                f_out.write("\n".join(new_lines) + "\n")

        count += 1

    print(f"{split}: merged {count} images")


for split in SPLITS:
    relabel_and_copy(split)

print("Done merging biryani into training_data/")