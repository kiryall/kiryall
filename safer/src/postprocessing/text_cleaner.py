from src.utils.data_utils import normalize_plate


def clean_plate_text(text: str) -> str:
    return normalize_plate(text)
