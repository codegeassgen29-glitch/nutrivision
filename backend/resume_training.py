# This script resumes training from the last saved checkpoint
# (in case training was interrupted, e.g. by a container restart).

from ultralytics import YOLO

model = YOLO("/app/training_runs/food_detector_v1/weights/last.pt")
model.train(resume=True)