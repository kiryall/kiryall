from pathlib import Path


def list_images(input_dir: str | Path, exts: tuple[str, ...]) -> list[Path]:
    root = Path(input_dir)
    return sorted([p for p in root.iterdir() if p.suffix in exts and p.is_file()])
