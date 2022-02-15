from calendar import month
import sys, os
import datetime, time

def clear():
    if sys.stdin and sys.stdin.isatty():  # Check if running from terminal
        # For windows the name is 'nt'
        if os.name == 'nt':
            os.system('cls')
        # For mac and linux, the os.name is 'posix'
        else:
            os.system('clear')

def accept_eula():
    Rfile = open(r"eula.txt", 'r+')
    if any(line.strip() == "eula=true" for line in Rfile):
        print("[INFO] [ZStart] eula.txt already true, skipping..")
    else:
        file = open(r"eula.txt", 'w+')
        print("[INFO] [ZStart] Accepting eula.txt..")
        lines = [
            "# Automatically accepted by ZStartup\n",
            "# By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n",
            "eula=true"
        ]
        file.truncate(0)
        file.writelines(lines)