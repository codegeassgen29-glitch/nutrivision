# This service handles running YOLOv8 object detection on food images.
#
# We use a PRETRAINED YOLOv8 model (trained on the COCO dataset).
# IMPORTANT LIMITATION: COCO only has a few food-related classes:
# banana, apple, sandwich, orange, broccoli, carrot, pizza, donut,
# cake, hot dog. It will NOT recognize most real dishes (biryani,
# dal, pasta, etc.) — that requires custom training, which we'll
# tackle in a later milestone.

from ultralytics import YOLO

# Load the model ONCE when this module is first imported (not per-request).
# Loading a model is slow (~1-2 seconds); reusing it across requests
# is far more efficient than reloading it every time someone uploads a photo.
# "yolov8n.pt" = the "nano" version - smallest and fastest, good for
# development. Larger versions (yolov8s, yolov8m, yolov8l, yolov8x)
# are more accurate but slower.
model = YOLO("yolov8n.pt")

# COCO class names that we consider "food" for this project.
# We filter detections down to just these, since COCO also detects
# things like "person", "car", "chair" etc. which aren't relevant here.
FOOD_CLASSES = {
    "banana", "apple", "sandwich", "orange", "broccoli",
    "carrot", "pizza", "donut", "cake", "hot dog",
}

# Minimum confidence score (0 to 1) to accept a detection.
# Lower = more detections but more false positives.
CONFIDENCE_THRESHOLD = 0.4


def detect_food(image_path: str) -> list[dict]:
    """
    Runs YOLOv8 on the given image and returns a list of detected foods.

    Args:
        image_path: full path to the image file on disk

    Returns:
        A list of dicts like:
        [{"food_name": "banana", "confidence": 0.87}, ...]
    """

    # Run inference. YOLO returns a list of "Results" objects
    # (one per image - we only pass one image, so we take [0]).
    results = model(image_path)
    result = results[0]

    detected_foods = []

    # Each detected object is a "box" with a class ID and confidence score.
    for box in result.boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]  # e.g. "banana"
        confidence = float(box.conf[0])     # e.g. 0.87

        # Only keep it if it's a food class AND confident enough
        if class_name in FOOD_CLASSES and confidence >= CONFIDENCE_THRESHOLD:
            detected_foods.append({
                "food_name": class_name,
                "confidence": round(confidence, 3),
            })

    return detected_foods