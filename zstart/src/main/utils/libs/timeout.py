import sys, time

from utils.libs import lx_term
from common.entry import write
from common.colors import HexFg

import instances

def timeout(seconds: int):
    """Wait for a key press or timeout after a specified number of seconds"""
    if not sys.stdin or not sys.stdin.isatty():
        return

    with lx_term.lxTERM() as lxTerm:
        start_time =  time.time()
        while True:
            time_left = max(0, seconds - int(time.time() - start_time))
            write(f"{instances.PREFIX} {HexFg("#7651f4")}Press any key to continue or wait",
                f"{HexFg("#bc74e3")}{time_left} {HexFg("#7651f4")}seconds ...", end='\r')
            if time_left == 0:
                write('\n')
                write(f"{HexFg("#f45158")}> Timed out ...\n")
                break
            elif lxTerm.kb_hit():
                write('\n')
                write(f"{HexFg("#f766c7")}> Skipping ...\n")
                break
            time.sleep(1)