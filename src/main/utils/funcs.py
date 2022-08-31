import sys, os
from sty import *
from select import select
from calendar import month
import datetime, time
from . import _vars

if os.name == 'nt':
    import msvcrt
else:
    import termios
    import atexit
    from select import select

def lx_init():
    if os.name != 'nt':
        global fd, old_term
        # Save the terminal settings
        fd = sys.stdin.fileno()
        new_term = termios.tcgetattr(fd)
        old_term = termios.tcgetattr(fd)
        # New terminal setting unbuffered
        new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)
        # Support normal-terminal reset at exit
        atexit.register(set_normal_term)

def set_normal_term():
    if os.name != 'nt':
        global fd, old_term
        termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

def getch():
    if os.name != 'nt':
        return sys.stdin.read(1)
    else:
        return msvcrt.getch()
def kbhit():
    if os.name != 'nt':
        dr,dw,de = select([sys.stdin], [], [], 0)
        return dr != []
    else:
        return msvcrt.kbhit()


def clear():
    if sys.stdin and sys.stdin.isatty():  # Check if running from terminal
        # For windows the name is 'nt'
        if os.name == 'nt':
            os.system('cls')
        # For mac and linux, the os.name is 'posix'
        else:
            os.system('clear')


def timeout(seconds):
    if sys.stdin and sys.stdin.isatty():  # Check if running from terminal
        lx_init()
        inp = None
        refer = None
        timeOut = seconds
        timeLeft = timeOut
        timeInit = time.time()
        while inp is None:
            timeDiff = int(time.time()-timeInit)
            if timeLeft != refer:
                plural = lambda x: "" if x == 1 else "s" 
                print(f"{fg(233,84,49)}Press any key to continue or wait {timeLeft} second{plural(timeLeft)}... ")
                refer = timeLeft
            if not timeOut-timeDiff < 0:
                timeLeft = timeOut-timeDiff
            else:
                timeLeft = 0

            if kbhit():
                inp = getch()
            elif timeLeft == 0:
                inp = 0
        print(rs.all)
        if inp:
            print(f"{fg.da_grey}[{fg.cyan}ZStart{fg.da_grey}] {fg.grey}Skipping...")
            if ord(inp) == 27:
                return True
        else:
            print(f"{fg.da_grey}[{fg.cyan}ZStart{fg.da_grey}] {fg.li_red}Timed out...")
        print(rs.all)
        set_normal_term()

def title(text):
    import ctypes
    if os.name == 'nt':
        try:
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.SetConsoleTitleW(text)
        except (WindowsError, IOError, RuntimeError):
            ctypes.WinError(ctypes.get_last_error())
            os.system(f'title {text}')
        os.system('color') # Compatibility color fix for windows terminals
    else:
        sys.stdout.write(b'\33]0; ' + text + b'\a')
        sys.stdout.flush()
        os.system("") # Compatibility color fix for other terminals



def accept_eula():
    if _vars.console["auto-eula"]:
        Rfile = open(r"eula.txt", 'r+')
        if any(line.strip() == "eula=true" for line in Rfile):
            print(f"{fg.da_grey}[{fg(218,116,32)}INFO{fg.da_grey}] {fg.li_red}eula.txt already true, skipping..")
        else:
            file = open(r"eula.txt", 'w+')
            print(f"{fg.da_grey}[{fg(218,116,32)}INFO{fg.da_grey}] {fg.green}Accepting eula.txt..")
            lines = [
                "# Automatically accepted by ZStartup\n",
                "# By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n",
                "eula=true"
            ]
            file.truncate(0)
            file.writelines(lines)


# New input system, replaces input()
def xinput(allowCMD=True, sep=">>>", color=fg(0, 148, 255), coloraf=rs.all):
    import traceback
    from io import TextIOWrapper
    from shlex import split as shlex_split

    try:
        print(f"{color}{sep}{coloraf} ", end='')
        cmd = input()
        print()
        #if isinstance(_vars.log_f, TextIOWrapper):
        #    _vars.log_f.write(cmd+"\n")
        #if _vars.configVars["clearMode"]:
        #    clear()
        #if allowCMD and len(cmd) > 0 and cmd[0] == "/":
        #    args = shlex_split(cmd)
        #    return runCommand(args)
        #else:
        return cmd
    except ValueError as e:
        if e.args[0] in "No closing quotation":
            print(f"{fg(196)}{fg.bold}Invalid input. No closing quotation.{rs.all}")
            print()
        else:
            print(f"{rs.all}‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
            print(f"{fg.li_red} [WARNING] Something awful happened!")
            print(f"{fg.da_grey} [{fg.yellow}INFO{fg.da_grey}] {fg.li_blue}Exception caught! {e.__class__}: {e.args[0]}")
            # Will print this message followed by traceback.
            print(f"{fg.red}{traceback.format_exc()}", end='')
            print(f"{rs.all}____________________________________________________________\n")