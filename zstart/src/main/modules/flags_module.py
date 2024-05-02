class FlagsModule:
    name: str
    enabled: bool
    overrides: list
    incompatible: list
    flags: list
    
    def __init__( modulePath: str ):
        ...
    