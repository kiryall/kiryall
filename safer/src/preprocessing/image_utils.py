import cv2
import numpy as np


def crop_polygon(image: np.ndarray, points: np.ndarray) -> np.ndarray:
    x, y, w, h = cv2.boundingRect(points.astype(np.int32))
    return image[y : y + h, x : x + w]


def read_image(path: str) -> np.ndarray:
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Cannot read image: {path}")
    return image
