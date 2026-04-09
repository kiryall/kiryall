import argparse
from pathlib import Path

from src.pipeline.batch_processor import process_batch


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", default="output")
    parser.add_argument("--threshold", type=float, default=0.9)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    results = process_batch(args.input_dir, args.output_dir, args.threshold, args.dry_run)
    print(f"Processed {len(results)} files")


if __name__ == "__main__":
    main()
