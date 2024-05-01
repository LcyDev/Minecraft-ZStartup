from dataclasses import dataclass, field

@dataclass
class LocalData:
    unstable: bool = True
    debug: bool = False
    restart: bool = False
    exitMenu: bool = False
    autoDisableExit: bool = False
    exceptionBuffer: list = field(default_factory=lambda: [])