import os, subprocess
from pathlib import Path

import instances

from instances import configData

from common.entry import write
from common.colors import wc, fg, rs, HexFg

from utils import useful

def change_cwd(path: str):
    path = Path(path).absolute()
    cwd = Path().absolute()

    if cwd == path:
        write(f"{instances.PREFIX} {fg.grey}Current Working directory: {HexFg("#f8a022")}{path}")
    else:
        write(f"{instances.PREFIX} {fg.grey}Working directory changed to: {HexFg("#f8a022")}{path}")
        os.chdir(path)

def accept_eula():
    path = Path('eula.txt')

    if path.is_file():
        write(f"{instances.INFO} {HexFg("#5879f3")}Skipping already existing eula.txt\n")
        return

    with open(path, 'w') as f:
        write(f"{instances.INFO} {fg.green}Accepting eula.txt ...\n")
        f.truncate(0)
        f.writelines([
            "# Automatically accepted by ZStart5\n",
            "# By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n",
            "eula=true"
        ])

def debug_cmd():
    jvm_memory = configData.get_jvm_mem()

    write(f'{HexFg("#d7204c")}"{configData.java.java_binary}" {HexFg("#ee38a6")}{jvm_memory[0]} {HexFg("#ee384c")}{jvm_memory[1]}')
    write()
    write(f"{HexFg("#64bea0")}{configData.get_jvm_flags()}")
    write()
    write(f'{HexFg("#82bab4")}{configData.get_jar_flags()} {fg.grey}-jar {HexFg("#2a70e8")}"{configData.get_exec_path()}" {HexFg("#72b4d2")}{configData.get_jar_args()}')
    write()

def get_cmd() -> list[str]:
    args = []

    args.append(configData.java.java_binary)
    args.extend(configData.get_jvm_mem())
    args.extend(configData.get_jvm_flags())
    args.extend(configData.get_jar_flags())
    args.append('-jar')
    args.append(configData.get_exec_path())
    args.extend(configData.get_jar_args())
    return args

def show_java_version():
    print(HexFg("#da5050"))
    subprocess.call([configData.java.java_binary, '-version'])
    print(rs.all)

def get_jar_path() -> Path:
    path = Path(configData.get_exec_path())

    if path.is_file():
        write(f"{instances.INFO} {fg.li_green}JAR executable was found...\n")
        return path.resolve()
    elif path.absolute().is_file():
        write(f"{instances.INFO} {fg.li_cyan}JAR executable found within ZStart path...\n")
        return path.resolve()
    else:
        write(f"{instances.WARN} {wc.warn}Couldn't find JAR executable.\n")

def run_server():
    if os.access(configData.java.java_binary, os.R_OK):
        print(HexFg("#d685cb"))
        subprocess.call(get_cmd())
        print(rs.all)
    else:
        write(f"{instances.WARN} {wc.warn}Can't access JAR executable, permission error?\n")

def loadParameters():
    write()
    write(f"{instances.INFO} {fg(216,190,80)}{useful.get_current_time()}")
    write(f"{fg.da_grey}[{fg.cyan}ZStart{fg.da_grey}] {fg.grey}Loading startup parameters...")
    write()

def startSRV():
    write()
    write(f"{instances.INFO} {fg(216,190,80)}{useful.get_current_time()}")
    write(f"{fg.da_grey}[{fg.cyan}ZStart{fg.da_grey}] {fg.grey}Starting Server...")
    write()