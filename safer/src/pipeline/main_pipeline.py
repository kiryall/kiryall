from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path

from configs.config import PipelineConfig
from src.detection.yolo_detector import YoloObbDetector
from src.grouping.exif_grouper import simple_group
from src.ocr.ocr_engine import PaddleOcrEngine
from src.postprocessing.text_cleaner import clean_plate_text
from src.postprocessing.validator import validate_plate
from src.preprocessing.image_loader import list_images
from src.renaming.renamer import apply_rename, make_new_name
from src.reporting.report_generator import save_report


@dataclass(slots=True)
class FileResult:
    input_name: str
    output_name: str
    plate_text: str
    confidence: float
    status: str
    group_id: str
    reason: str


class MainPipeline:
    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self.detector = YoloObbDetector(config.yolo_model_path, config.detection_conf_threshold)
        self.ocr = PaddleOcrEngine()

    def run(self, input_dir: str | Path, output_dir: str | Path, dry_run: bool = True) -> list[FileResult]:
        images = list_images(input_dir, self.config.input_extensions)
        groups = simple_group(images)
        counters: defaultdict[str, int] = defaultdict(int)
        results: list[FileResult] = []

        for group_id, files in groups.items():
            for image_path in files:
                detection = self.detector.detect_plate(image_path)
                if not detection.found:
                    results.append(
                        FileResult(
                            input_name=image_path.name,
                            output_name=f"{self.config.unknown_prefix}{image_path.name}",
                            plate_text="",
                            confidence=0.0,
                            status="group_3_unrecognized",
                            group_id=group_id,
                            reason=detection.reason or "no_detection",
                        )
                    )
                    continue

                ocr_result = self.ocr.read(detection.crop)
                plate = clean_plate_text(ocr_result.text)
                valid = validate_plate(plate)
                conf = min(detection.confidence, ocr_result.confidence)

                if not ocr_result.success or not valid:
                    results.append(
                        FileResult(
                            input_name=image_path.name,
                            output_name=f"{self.config.unknown_prefix}{image_path.name}",
                            plate_text=plate,
                            confidence=conf,
                            status="group_3_unrecognized",
                            group_id=group_id,
                            reason="invalid_ocr",
                        )
                    )
                    continue

                new_name = make_new_name(plate, counters, image_path.suffix.lower())
                if conf < self.config.confidence_threshold:
                    new_name = f"{self.config.low_conf_prefix}{new_name}"
                    status = "group_2_low_confidence"
                    reason = "below_threshold"
                else:
                    status = "group_1_ok"
                    reason = ""

                apply_rename(image_path, Path(output_dir) / new_name, dry_run=dry_run)
                results.append(
                    FileResult(
                        input_name=image_path.name,
                        output_name=new_name,
                        plate_text=plate,
                        confidence=conf,
                        status=status,
                        group_id=group_id,
                        reason=reason,
                    )
                )

        save_report([asdict(r) for r in results], Path(output_dir) / "results.csv")
        return results
