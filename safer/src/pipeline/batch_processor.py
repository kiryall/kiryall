from pathlib import Path

from configs.config import PipelineConfig
from src.pipeline.main_pipeline import MainPipeline


def process_batch(input_dir: str | Path, output_dir: str | Path, threshold: float, dry_run: bool):
    cfg = PipelineConfig(confidence_threshold=threshold)
    pipeline = MainPipeline(cfg)
    return pipeline.run(input_dir, output_dir, dry_run=dry_run)
