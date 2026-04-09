from src.utils.data_utils import is_valid_plate


def validate_plate(text: str) -> bool:
    return is_valid_plate(text)
