import datetime
from pathlib import Path

def get_percentage(value: int, percentage: int) -> int:
    """Return the percentage of a given value as an integer."""
    percent: float = percentage / 100
    return int(value * percent)

def slith(value: str | list[str]) -> list[str]:
    """If the argument is a string, it is split from spaces and converted into a list."""
    if isinstance(value, str):
        return value.split(' ')
    else:
        return value

def get_current_time() -> str:
    return datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

def normalize_keys(x: dict):
    return {
        k.replace("-", "_"): normalize_keys(v) if isinstance(v, dict) else v
        for k, v in x.items()
    }

def update_dict(original: dict, new: dict, only_existing: bool = True):
    for k, v in only_existing.items():
        if k in original:
            if isinstance(original[k], dict) and isinstance(v, dict):
                update_dict(original[k], original[v])
            else:
                original[k] = v
        elif not only_existing:
            original[k] = v