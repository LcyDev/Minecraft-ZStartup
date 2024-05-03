class FlagsGroup:
    name: str
    enabled: bool
    overrides: list
    incompatible: list[str]
    flags: list[str]
    
    def __init__(  ):
        ...


class FlagsModule:
    name: str
    enabled: bool
    incompatible: list[str]
    groups: list[FlagsGroup]
    
    def __init__( modulePath: str ):
        ...
    