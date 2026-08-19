# This service handles running YOLOv8 object detection on food images.
#
# We run TWO models together:
# 1. A PRETRAINED model (COCO) - recognizes general foods like pizza,
#    banana, sandwich, etc.
# 2. Our CUSTOM-TRAINED model - recognizes specific dishes we trained it
#    on: chapati, dal makhni, fried rice, kadai paneer.
#
# Running both gives broader coverage than either alone. Later, as we
# add more custom classes, the custom model's coverage will grow.

from ultralytics import YOLO

# Pretrained model - loaded once at import time
pretrained_model = YOLO("yolov8n.pt")

# Our custom-trained model - loaded once at import time
custom_model = YOLO("/app/models/food_detector_v1.pt")

# COCO classes we consider "food"
COCO_FOOD_CLASSES = {
    "banana", "apple", "sandwich", "orange", "broccoli",
    "carrot", "pizza", "donut", "cake", "hot dog",
}

CONFIDENCE_THRESHOLD = 0.4
CUSTOM_CONFIDENCE_THRESHOLD = 0.3  # slightly lower - our custom model is smaller/less mature


def detect_food(image_path: str) -> list[dict]:
    """
    Runs both the pretrained and custom models on the given image,
    and returns a combined list of detected foods.
    """
    detected_foods = []

    # --- Pretrained model (COCO classes) ---
    results = pretrained_model(image_path)
    result = results[0]

    for box in result.boxes:
        class_id = int(box.cls[0])
        class_name = pretrained_model.names[class_id]
        confidence = float(box.conf[0])

        if class_name in COCO_FOOD_CLASSES and confidence >= CONFIDENCE_THRESHOLD:
            detected_foods.append({
                "food_name": class_name,
                "confidence": round(confidence, 3),
            })

    # --- Custom model (our trained Indian food classes) ---
    custom_results = custom_model(image_path)
    custom_result = custom_results[0]

    for box in custom_result.boxes:
        class_id = int(box.cls[0])
        class_name = custom_model.names[class_id]
        confidence = float(box.conf[0])

        if confidence >= CUSTOM_CONFIDENCE_THRESHOLD:
            detected_foods.append({
                "food_name": class_name,
                "confidence": round(confidence, 3),
            })

    return detected_foods