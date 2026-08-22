from ultralytics import YOLO

model = YOLO("/app/training_runs/food_detector_v2/weights/last.pt")
model.train(resume=True)