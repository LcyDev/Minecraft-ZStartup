import yaml

from dataclasses import dataclass, field

from pathlib import Path

from utils import useful

class Group:
    name: str
    enabled: bool
    overrides: list[str]
    flags: list[str]

class Module:
    groups: list[Group]

def get_modules(path: str, modules: str | list[str]):
    modules = useful.slith(modules)

    for module in modules:
        if not Path(path / module).exists():
            print(f"Module {module} not found in {path}.")
            continue
