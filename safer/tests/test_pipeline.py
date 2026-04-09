from pathlib import Path

from configs.config import PipelineConfig
from src.pipeline.main_pipeline import MainPipeline


class DummyDetector:
    def detect_plate(self, _):
        class R:
            found = False
            confidence = 0.0
            reason = "no_detection"
            crop = None

        return R()


class DummyOCR:
    def read(self, _):
        raise AssertionError("OCR should not be called when detection is empty")


def test_pipeline_no_detection(tmp_path: Path):
    input_dir = tmp_path / "in"
    output_dir = tmp_path / "out"
    input_dir.mkdir()
    output_dir.mkdir()
    (input_dir / "img1.jpg").write_bytes(b"123")

    pipeline = MainPipeline(PipelineConfig())
    pipeline.detector = DummyDetector()
    pipeline.ocr = DummyOCR()

    results = pipeline.run(input_dir, output_dir, dry_run=True)

    assert len(results) == 1
    assert results[0].status == "group_3_unrecognized"
    assert results[0].confidence == 0.0
