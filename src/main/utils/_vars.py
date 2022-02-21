# constantes
__VERSION__ = "1.0-beta"
import os
import re
import toml
import yaml
from sty import *
from . import alt_funcs



def init():
    init_yaml()
    setVars()


def init_yaml():
    global config, console, server, java, flags
    if not os.path.exists('config.yml'):
        pass #generate file
    with open('config.yml', 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            console = config['console']
            server = config['server']
            java = config['java']
            flags = java['flags']

def setVars():
    global JAVA_PATH, JAVA_MEM, JAVA_FLAGS
    global JAR_FLAG, JAR_PATH, JAR_ARGS
    global PRINT_JAVA, PRINT_FLAGS, PRINT_JAR, RUN_CMD
    xms = int(java["max-memory"] * java["memory-percent"] / 100)
    xmx = int(java["max-memory"] * java["memory-percent"] / 100)
    enabledFlags = flags["enabled"].replace(', ', ',')

    JAVA_PATH = java["java-binary"]
    JAVA_MEM = [f'-Xms{xms}{java["heap-unit"][0]}', f'-Xmx{xmx}{java["heap-unit"][0]}']
    JAVA_FLAGS = flags["defaults"]
    if isinstance(JAVA_FLAGS, str):
        JAVA_FLAGS = flags["defaults"].split(' ')
    for i in re.split(r', |,', flags["enabled"]):
        flag = flags[i]["list"]
        if isinstance(flag, str): 
            JAVA_FLAGS.extend(flag.split(' '))
        else:
            JAVA_FLAGS.extend(flag)
    
    JAR_PATH = server["jar-path"]+server["jar-name"]
    
    JAR_FLAGS = []
    if server["eula-skip"]:
        JAR_FLAGS.append("-DCom.mojang.eula.agree=true")
    if isinstance(server["before-jar"], str):
        JAR_FLAGS.extend(server["before-jar"].split(' '))

    if isinstance(server["parameters"], str):
        JAR_ARGS = server["parameters"].split(' ')
    else:
        JAR_ARGS = server["parameters"]

    RUN_CMD = [JAVA_PATH, *JAVA_MEM, *JAVA_FLAGS, *JAR_FLAGS, '-jar', JAR_PATH, *JAR_ARGS]
    PRINT_JAVA = f'{fg(215,32,76)}"{JAVA_PATH}" {fg(238,62,120)}{JAVA_MEM[0]} {fg(230,26,100)}{JAVA_MEM[1]}'
    PRINT_FLAGS = f"{fg(100,190,160)}{alt_funcs.join(JAVA_FLAGS)}"
    PRINT_JAR =  f'{fg(130,184,178)}{alt_funcs.join(JAR_FLAGS)} {fg.grey}-jar {fg(42,112,232)}"{JAR_PATH}" {fg(114,180,210)}{alt_funcs.join(JAR_ARGS)}'

def init_toml():
    if not os.path.exists('config.toml'):
        pass #generate file
    else: 
        with open('config.toml', 'r') as f:
            config = toml.load(f)