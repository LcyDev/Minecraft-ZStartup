import os, sys, ctypes, traceback
import sty
from sty import *
import ZStart
from utils import _vars, funcs, alt_funcs

if os.name == 'nt':
    from msvcrt import getch
else:
    import getch

def setup():
    funcs.title(f"ZStartup5 - {_vars.__VERSION__}")

def main():
    try:
        funcs.clear()
        print(f"{fg.da_grey}[{fg.cyan}ZStart{fg.da_grey}] {fg(233,50,106)}Loading ZStart5 version {_vars.__VERSION__}...\n")
        _vars.init()
        
        ZStart.setup()
        funcs.accept_eula()
        ZStart.initLoop()
    except Exception:
        print(f"{rs.all}\n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
        print(f"{fg.li_red} [WARNING] Something awful happened!")
        # Will print this message followed by traceback.
        print(f"{fg.red}{traceback.format_exc()}", end='')
        print(f"{rs.all}____________________________________________________________\n")
        print(f"{fg.li_red}Press any key to exit the program.{rs.all}")
        getch()
        print()
        raise

if __name__ == "__main__":
    setup()
    main()
