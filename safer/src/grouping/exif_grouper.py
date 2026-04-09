from pathlib import Path


def simple_group(images: list[Path]) -> dict[str, list[Path]]:
    """MVP grouping: one group by sorted order.

    Can be replaced by EXIF time-window grouping.
    """
    return {"group_001": sorted(images)}
