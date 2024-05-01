import sty

from sty import Style, Register
from sty import fg, bg, ef, rs
from sty import Sgr, RgbFg, RgbBg

def hex_to_rgb(hex_code: str) -> list[int]:
    # Normalize input
    hex_code = hex_code.lower().lstrip('#')

    # Convert the hex color code to RGB values
    rgb_list = [
        int(hex_code[i:i+2], base=16)
        for i in range(0, len(hex_code), 2)
    ]
    # Ensure that all RGB values are in the range of 0-255
    if not all(0 <= rgb <= 255 for rgb in rgb_list):
        return []

    return rgb_list

def HexFg(hex_code: str) -> Style:
    return fg(*hex_to_rgb(hex_code))

def HexBg(hex_code: str) -> Style:
    return bg(*hex_to_rgb(hex_code))

class wColor:
    info = HexFg('#ede34e')
    fine = HexFg('#4eed6f')
    alert = HexFg('#ec7530')
    warn = HexFg('#ec482f')
    fatal = HexFg('#ff0000')

    mistake = HexFg('#e65d5d')
    error = HexFg('#cb0c0c')

    red = HexFg('#c40000')
    green = HexFg('#00c800')
    blue = HexFg('#0046c8')
    yellow = HexFg('#ffec00')

wc = wColor()