#!/usr/bin/env python
import os, sys
from pathlib import Path

# Set environment variables
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Constants
IS_COMPILED = False
ICON_PATH = "../lib/wood.ico"

# Program
import instances, versions

from common import entry
from common.entry import write
from common.colors import wc, fg, HexFg

from utils.libs import lx_term

def setup():
    if IS_COMPILED:
        entry.load_icon(ICON_PATH)
    entry.set_title(f"ZStart - {versions.SOFTWARE_VERSION}")

def start():
    ...

def main():
    setup()
    lxTerm = lx_term.lxTERM()
    try:
        entry.clear()
        write(f"{instances.PREFIX} {HexFg("#e9326a")}Loading ZStart version {versions.SOFTWARE_VERSION} ...\n")
        start()
        if instances.localData.restart:
            write(f"{wc.warn}Press any key to restart the game.")
            lxTerm.getch()
            main()
    except Exception as e:
        entry.handle_exception(e, output="BOTH")
        raise
    finally:
        write(f"{wc.warn}Press any key to exit the program.")
        lxTerm.getch()

if __name__ == "__main__":
    main()
