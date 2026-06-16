import torch
import time
from PIL import Image
import os

model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/best.pt')
model.conf = 0.5

image_folder = 'test_images'   # folder with your test images
times = []

for img_file in os.listdir(image_folder):
    img = Image.open(os.path.join(image_folder, img_file))
    start = time.time()
    results = model(img, size=640)
    times.append(time.time() - start)

avg_fps = 1 / (sum(times) / len(times))
print(f"Average FPS: {avg_fps:.1f}")