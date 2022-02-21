import os, sys, ctypes, traceback #system
import sty # colors
from sty import * 
from msvcrt import getch # to Press any key to continue
import ZStart
from utils import _vars, funcs, alt_funcs # Local imports


def setup():
    if os.name == 'nt':
        try:
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.SetConsoleTitleW(f"ZStartup5 - {_vars.__VERSION__}")
        except (WindowsError, IOError, RuntimeError):
            ctypes.WinError(ctypes.get_last_error())
            os.system(f'title ZStartup5 - {_vars.__VERSION__}')
        os.system('color') # Compatibility color fix for windows terminals
    else:
        sys.stdout.write(b'\33]0; ZStartup5 - ' + _vars.___VERSION__ + b'\a')
        sys.stdout.flush()
        os.system("") # Compatibility color fix for other terminals

def main():
    try:
        os.system("cls")
        print()
        _vars.init()
        #input(">> ")
        ZStart.startSRV()
        #funcs.accept_eula()
        pass
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
