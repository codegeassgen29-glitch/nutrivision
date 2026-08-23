# This service handles running YOLOv8 object detection on food images.
#
# We run TWO models together:
# 1. A PRETRAINED model (COCO) - recognizes general foods like pizza,
#    banana, sandwich, etc.
# 2. Our CUSTOM-TRAINED model (v2) - recognizes 21 Indian food classes.
#    Trained on a merged dataset from multiple sources. See training
#    notes: some classes (Chole, chicken, palak_paneer) perform well;
#    others (kadai_paneer, roti, samosa) are weak and need more/better
#    training data in a future iteration.

from ultralytics import YOLO

# Pretrained model - loaded once at import time
pretrained_model = YOLO("yolov8n.pt")

# Our custom-trained model (v2, 21 classes) - loaded once at import time
custom_model = YOLO("/app/models/food_detector_v2.pt")

# COCO classes we consider "food"
COCO_FOOD_CLASSES = {
    "banana", "apple", "sandwich", "orange", "broccoli",
    "carrot", "pizza", "donut", "cake", "hot dog",
}

CONFIDENCE_THRESHOLD = 0.6
CUSTOM_CONFIDENCE_THRESHOLD = 0.3


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

    # --- Custom model (our trained Indian food classes, v2: 21 classes) ---
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