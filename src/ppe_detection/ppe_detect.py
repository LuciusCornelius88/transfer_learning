import cv2
import shutil
import math
import cvzone
from ultralytics import YOLO
from pathlib import Path


WINDOW_NAME = 'Window'
VIDEO_PATH = './data/videos/'
MODEL_PATH = './yolo_weights/'
CLASS_NAMES = ['Excavator', 'Gloves', 'Hardhat', 'Ladder', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person',
               'SUV', 'Safety Cone', 'Safety Vest', 'bus', 'dump truck', 'fire hydrant', 'machinery', 'mini-van', 'sedan',
               'semi', 'trailer', 'truck and trailer', 'truck', 'van', 'vehicle', 'wheel loader']


def delecte_cache(input_path):
    for path in input_path.iterdir():
        if path.is_dir() and path.name == '__pycache__':
            shutil.rmtree(path)
        elif path.is_dir():
            delecte_cache(path)


def main():
    model = YOLO(f'{MODEL_PATH}ppe_detect_weights.pt')
    cap = cv2.VideoCapture(f'{VIDEO_PATH}ppe_2.mp4')
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    cv2.namedWindow(WINDOW_NAME)

    while True:
        ret, img = cap.read()

        if not ret:
            break

        results = model(img, stream=True)
        for res in results:
            for box in res.boxes:
                x1, y1, x2, y2 = (int(item) for item in box.xyxy[0])
                w, h = x2 - x1, y2 - y1

                conf = math.ceil(box.conf[0] * 100) / 100
                cls = int(box.cls[0])
                current_class = CLASS_NAMES[cls]

                if conf > 0.5:
                    if current_class in ['NO-Hardhat', 'NO-Mask', 'NO-Safety Vest']:
                        color = (0, 0, 255)
                    elif current_class in ['Hardhat', 'Mask', 'Safety Vest']:
                        color = (0, 255, 0)
                    else:
                        color = (255, 0, 0)

                    if w <= 170:
                        x_pos = x1 + w // 2
                    else:
                        x_pos = x1

                    cvzone.cornerRect(img, (x1, y1, w, h), l=5, t=2, rt=2, colorR=color)
                    cvzone.putTextRect(img, f'{current_class}: {conf}', (max(0, x_pos), max(35, y1)),
                                       scale=1, thickness=1, colorT=(255, 255, 255), colorB=color)

        cv2.imshow(WINDOW_NAME, img)

        key = cv2.waitKey(1)
        if key == ord(' '):
            break
        elif key == ord('p'):
            cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()
    delecte_cache(Path(__file__).parent.parent)


if __name__ == '__main__':
    main()
