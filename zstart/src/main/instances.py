from common.colors import fg, HexFg

from objects.data import LocalData, ConfigData

localData = LocalData()
configData = ConfigData()

PREFIX: str = f'{fg.da_grey}[{HexFg("#4267ee")}ZStart5{fg.da_grey}]'
INFO: str = f'{fg.da_grey}[{HexFg("#f0be19")}INFO{fg.da_grey}]'
WARN: str = f'{fg.da_grey}[{HexFg("#fd533a")}WARN{fg.da_grey}]'
