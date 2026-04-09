from collections import defaultdict
from pathlib import Path


def make_new_name(base_plate: str, counters: defaultdict[str, int], suffix: str = ".jpg") -> str:
    counters[base_plate] += 1
    return f"{base_plate}_{counters[base_plate]}{suffix}"


def apply_rename(src: Path, dst: Path, dry_run: bool = True) -> None:
    if dry_run:
        return
    src.rename(dst)
