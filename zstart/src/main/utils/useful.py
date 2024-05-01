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

def get_modules(path: str, modules: str | list[str]):
    modules = slith(modules)

    for module in modules:
        if not Path(path / module).exists():
            print(f"Module {module} not found in {path}.")
            continue