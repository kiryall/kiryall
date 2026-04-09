from dataclasses import dataclass
from pathlib import Path

import numpy as np

from src.preprocessing.image_utils import crop_polygon, read_image
from src.utils.logger import get_logger

try:
    from ultralytics import YOLO
except Exception:  # pragma: no cover
    YOLO = None


logger = get_logger(__name__)


@dataclass(slots=True)
class DetectionResult:
    found: bool
    crop: np.ndarray | None
    confidence: float
    reason: str = ""


class YoloObbDetector:
    def __init__(self, model_path: str | Path, conf_threshold: float = 0.1) -> None:
        self.model_path = Path(model_path)
        self.conf_threshold = conf_threshold
        self.model = None
        if YOLO is not None and self.model_path.exists():
            self.model = YOLO(str(self.model_path))
        else:
            logger.warning("YOLO model unavailable: %s", self.model_path)

    def detect_plate(self, image_path: str | Path) -> DetectionResult:
        if self.model is None:
            return DetectionResult(False, None, 0.0, "no_detection_model")

        image = read_image(str(image_path))
        result = self.model.predict(source=image, conf=self.conf_threshold, verbose=False)[0]
        obb = getattr(result, "obb", None)
        if obb is None or len(obb) == 0:
            return DetectionResult(False, None, 0.0, "no_detection")

        confidences = obb.conf.cpu().numpy()
        idx = int(np.argmax(confidences))
        points = obb.xyxyxyxy[idx].cpu().numpy()
        crop = crop_polygon(image, points)
        return DetectionResult(True, crop, float(confidences[idx]))
