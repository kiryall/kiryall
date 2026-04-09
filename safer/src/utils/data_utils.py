import re

PLATE_PATTERN = re.compile(r"^\d{1,4}[abcde]?$", re.IGNORECASE)


def normalize_plate(text: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z]", "", text).lower().replace("t", "1")
    return cleaned


def is_valid_plate(text: str) -> bool:
    return bool(PLATE_PATTERN.match(text))
