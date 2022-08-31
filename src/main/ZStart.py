from concurrent.futures import process
import os, sys, ctypes, subprocess
from sty import *
from datetime import datetime as dt
from utils import _vars, funcs


def setup():
    funcs.title(_vars.console["title"])
    if not os.path.samefile(os.getcwd(), _vars.console["server-path"]):
        os.chdir(_vars.console["server-path"])
        print(f"{fg.da_grey}[{fg.cyan}ZStart{fg.da_grey}] {fg.grey}Working directory changed to: {fg(220,144,22)}{os.path.abspath(os.getcwd())}")
    else:
        print(f"{fg.da_grey}[{fg.cyan}ZStart{fg.da_grey}] {fg.grey}Current Working directory: {fg(220,144,22)}{os.path.abspath(os.getcwd())}")


def menuLoop():
    pass

def initLoop(inLoop=True):
    while inLoop:
        startSRV()
        if _vars.console["wait-mode"].upper() == "WAIT":
            if isinstance(_vars.console["wait-timer"], int):
                print(f"{fg.da_grey}[{fg.cyan}ZStart{fg.da_grey}] {fg.li_grey}Press ESC to prompt ZStart Menu.")
                c_ord = funcs.timeout(int(_vars.console["wait-timer"]))
                if c_ord:
                    funcs.xinput()
                    #menuLoop()
                    exit()
            else:
                print(f"{fg.da_grey}[{fg.li_red}WARN{fg.da_grey}] {fg.red}Wait-Timer can only be a integer value.{rs.all}")
        elif _vars.console["wait-mode"].upper() == "PAUSE":
            funcs.xinput()
            #menuLoop()
        elif _vars.console["wait-mode"].upper() == "NONE":
            pass
        if _vars.console["restart-loop"]:
            inLoop = True
    if _vars.console["exit-on-stop"]:
        exit()

def startSRV():
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

    altpath = os.path.join(_vars.__PATH__, _vars.JAR_PATH.replace('//', '\\').replace('/', '\\'))
    if os.path.isfile(_vars.JAR_PATH):
        print(f"{fg.da_grey}[{fg(218,116,32)}INFO{fg.da_grey}] {fg.li_green}JAR executable was found...")
    elif os.path.isfile(altpath):
        print(f"{fg.da_grey}[{fg(218,116,32)}INFO{fg.da_grey}] {fg.li_cyan}JAR executable found within ZStart path...")
        _vars.JAR_PATH = altpath
        _vars.RUN_CMD = [_vars.JAVA_PATH, *_vars.JAVA_MEM, *_vars.JAVA_FLAGS, *_vars.JAR_FLAGS, '-jar', _vars.JAR_PATH, *_vars.JAR_ARGS]
    else:
        print(f"{fg.da_grey}[{fg.li_red}WARN{fg.da_grey}] {fg.red}Couldn't find JAR executable.{rs.all}")
    
    if os.access( _vars.JAR_PATH, os.R_OK):
        print(fg(232,116,216))
        subprocess.call(_vars.RUN_CMD)
        print(rs.all)
    else:
        print(f"{fg.da_grey}[{fg.li_red}WARN{fg.da_grey}] {fg.red}Can't access JAR executable, permission error?.{rs.all}")
        pass