import os, sys, ctypes, subprocess
from sty import *
from datetime import datetime as dt
from utils import _vars


def setup():
    pass

def startSRV():
    if os.name == 'nt':
        try:
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.SetConsoleTitleW(f'{_vars.console["title"]}')
        except (WindowsError, IOError, RuntimeError):
            ctypes.WinError(ctypes.get_last_error())
            os.system(f'{_vars.console["title"]}')
        os.system('color') # Compatibility color fix for windows terminals
        os.chdir(_vars.console["server-path"])
        print(f"{fg.da_grey}[{fg.cyan}ZStart{fg.da_grey}] {fg.grey}Working directory changed to: {fg(220,144,22)}{os.path.abspath(os.getcwd())}")
    else:
        sys.stdout.write(b'\33]0; ' + _vars.console["title"] + b'\a')
        sys.stdout.flush()
        os.system("") # Compatibility color fix for other terminals
        os.chdir(_vars.console["server-path"])
    
    now = dt.now().strftime("%d/%m/%Y - %H:%M:%S")
    print()
    print(f"{fg.da_grey}[{fg(218,116,32)}INFO{fg.da_grey}] {fg(216,190,80)}{now}")
    print(f"{fg.da_grey}[{fg.cyan}ZStart{fg.da_grey}] {fg.grey}Loading startup parameters...")
    print()
    
    #print(fg.li_cyan + str(_vars.RUN_CMD) + rs.all)
    #print()
    print(_vars.PRINT_JAVA + rs.all)
    print(_vars.PRINT_FLAGS + rs.all)
    print(_vars.PRINT_JAR + rs.all)
    print(fg(218,80,80  ))
    os.system(f'"{_vars.JAVA_PATH}" -version')
    print(rs.all)
    print(f"{fg.da_grey}[{fg(218,116,32)}INFO{fg.da_grey}] {fg(216,190,80)}{now}")
    print(f"{fg.da_grey}[{fg.cyan}ZStart{fg.da_grey}] {fg.grey}Starting Server...")
    print(rs.all)
    #subprocess.call(_vars.RUN_CMD)
    print()
