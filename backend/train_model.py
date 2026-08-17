# This script trains a CUSTOM YOLOv8 model on our own food dataset
# (chapati, dal makhni, fried rice, kadai paneer), starting from
# YOLOv8's pretrained weights (transfer learning - not training from scratch).
#
# Run this INSIDE the Docker container, since that's where all our
# dependencies (torch, ultralytics) are installed.

from ultralytics import YOLO

# Start from the pretrained "nano" model - it already knows general
# shapes/edges/textures from millions of images. We're fine-tuning it
# to also recognize our specific food classes, which is much faster
# and needs far less data than training from zero.
model = YOLO("yolov8n.pt")

# Train the model on our dataset.
results = model.train(
    data="/app/training_data/data.yaml",  # tells YOLO where images + labels + class names are
    epochs=50,          # how many full passes through the training data
    imgsz=640,           # image size YOLO resizes everything to (matches Roboflow's export)
    batch=8,              # how many images processed at once (lower = less RAM/GPU needed)
    project="/app/training_runs",  # where to save results
    name="food_detector_v1",        # this run's folder name
    patience=10,           # stop early if no improvement for 10 epochs (saves time)
)

print("Training complete! Best weights saved at:")
print(results.save_dir)