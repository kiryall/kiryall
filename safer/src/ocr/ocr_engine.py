from dataclasses import dataclass

import cv2

from src.utils.logger import get_logger

try:
    from paddleocr import PaddleOCR
except Exception:  # pragma: no cover
    PaddleOCR = None


logger = get_logger(__name__)


@dataclass(slots=True)
class OcrResult:
    text: str
    confidence: float
    success: bool


class PaddleOcrEngine:
    def __init__(self) -> None:
        self.reader = None
        if PaddleOCR is not None:
            self.reader = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
        else:
            logger.warning("PaddleOCR is not installed; OCR returns empty")

    def read(self, image) -> OcrResult:
        if self.reader is None:
            return OcrResult("", 0.0, False)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        output = self.reader.ocr(gray, cls=True)
        if not output or not output[0]:
            return OcrResult("", 0.0, False)

        texts = []
        confs = []
        for line in output[0]:
            text, conf = line[1][0], float(line[1][1])
            texts.append(text)
            confs.append(conf)

        joined = "".join(texts)
        return OcrResult(joined, min(confs) if confs else 0.0, bool(texts))
