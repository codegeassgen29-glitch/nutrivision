from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.train(
    data="/app/training_data/data.yaml",
    epochs=30,             # reasonable ceiling given our time budget; early stopping will cut it short if it converges sooner
    imgsz=416,
    batch=8,
    project="/app/training_runs",
    name="food_detector_v2",
    patience=10,
)

print("Training complete! Best weights saved at:")
print(results.save_dir)