from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class PipelineConfig:
    yolo_model_path: Path = Path("models/yolo/v1/best.pt")
    confidence_threshold: float = 0.90
    detection_conf_threshold: float = 0.10
    input_extensions: tuple[str, ...] = (".jpg", ".jpeg", ".JPG", ".JPEG")
    unknown_prefix: str = "!"
    low_conf_prefix: str = "!"
    keep_original_on_fail: bool = True
