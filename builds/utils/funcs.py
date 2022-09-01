import os, sys
from sty import *

# Colors
def log(text, cancel=False):
    if not cancel:
        print(f"{fg.li_grey}{text}{fg.rs}")
def warn(text, cancel=False):
    if not cancel:
        print(f"{fg.li_red}{text}{fg.rs}")
def red(text, cancel=False):
    if not cancel:
        print(f"{fg(196)}{ef.bold}{text}{rs.all}")
def green(text, cancel=False):
    if not cancel:
        print(f"{fg(0,200,0)}{ef.bold}{text}{rs.all}")
def yellow(text, cancel=False):
    if not cancel:
        print(f"{fg(255,236,0)}{bg.rs}{text}{rs.all}")

# Misc else function.
def elseval(action=""):
    if isinstance(action, str):
        if action == "":
            warn("Invalid input, try again.\n")
        else:
            red("I don't understand what you're saying\n")
    elif isinstance(action, int):
        red("I don't understand what you're saying\n")

# Clear console function.
def clear(space=True):
    if sys.stdin and sys.stdin.isatty():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    if space:
        print()

# Misc function to convert str to bool
def strToBool(string):
    if isinstance(string, str):
        if string.lower() in {"true","1"}:
            return True
        if string.lower() in {"false","0"}:
            return False

def mPrint(num, text, menu=False):
    if None in (num, text):
        return
    print(f"{fg.rs}{num} {fg.cyan}{text}{fg.rs}")

def xinput(allowCMD=True, sep=">>>", color=fg(0, 148, 255), color2=rs.all):
    print(f"{color}{sep}{color2} ", end='')
    cmd = input().strip()
    print()
    return cmd