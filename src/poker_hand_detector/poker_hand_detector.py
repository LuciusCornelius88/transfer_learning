import cv2
import math
import shutil
import cvzone
from ultralytics import YOLO
from pathlib import Path

from poker_hand_function import find_poker_hand


WINDOW_NAME = 'Window'
MODEL_PATH = './yolo_weights/'
CLASS_NAMES = ['10C', '10D', '10H', '10S',
               '2C', '2D', '2H', '2S',
               '3C', '3D', '3H', '3S',
               '4C', '4D', '4H', '4S',
               '5C', '5D', '5H', '5S',
               '6C', '6D', '6H', '6S',
               '7C', '7D', '7H', '7S',
               '8C', '8D', '8H', '8S',
               '9C', '9D', '9H', '9S',
               'AC', 'AD', 'AH', 'AS',
               'JC', 'JD', 'JH', 'JS',
               'KC', 'KD', 'KH', 'KS',
               'QC', 'QD', 'QH', 'QS'
               ]


def delecte_cache(input_path):
    for path in input_path.iterdir():
        if path.is_dir() and path.name == '__pycache__':
            shutil.rmtree(path)
        elif path.is_dir():
            delecte_cache(path)


def main():
    model = YOLO(f'{MODEL_PATH}poker_detect_weights.pt')
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    while True:
        ret, img = cap.read()
        # img = cv2.flip(img, 180)

        if not ret:
            break

        hand = []
        results = model(img, stream=True)
        for res in results:
            for box in res.boxes:
                x1, y1, x2, y2 = (int(item) for item in box.xyxy[0])
                w, h = x2 - x1, y2 - y1

                cvzone.cornerRect(img, (x1, y1, w, h))

                conf = math.ceil(box.conf[0] * 100) / 100
                cls = int(box.cls[0])
                current_class = CLASS_NAMES[cls]

                cvzone.putTextRect(img, f'{current_class}: {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

                if conf > 0.35:
                    hand.append(current_class)

        hand = list(set(hand))
        if len(hand) == 5:
            poker_hand = find_poker_hand(hand)
            cvzone.putTextRect(img, f'Your Hand: {poker_hand}', (300, 75), scale=3, thickness=5)

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
