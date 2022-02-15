# constantes
__VERSION__ = "1.0-beta"
import os
import toml
from . import alt_funcs

def init():
    if not os.path.exists('config.toml'):
        pass #generate file
    else: 
        with open('config.toml', 'r') as f:
            config = toml.load(f)
            console = config['console']
            server = config['server']
            java = config['java']
            flags = config['flags']
            enableds = flags["enabled"].replace(', ', ',')
            javaflags = alt_funcs.join(flags["defaults"])
            for i in enableds.split(","):
                flag = alt_funcs.join(config[i]["flags"])
                if javaflags == "":
                    javaflags = flag
                else:
                    javaflags = f"{javaflags} {flag}"
            xms = int(java["max-memory"] * java["memory-percent"] / 100)
            xmx = int(java["max-memory"] * java["memory-percent"] / 100)
            CMD_JAVA = f"{java['java-binary']} -Xms{xms}{java['heap-unit'][0]} -Xmx{xmx}{java['heap-unit'][0]}"
            CMD_JAR = f"-jar \"{server['jar-path']+server['jar-name']}\" {}{alt_funcs.join(server['parameters'])}"
            print(CMD_JAVA)
            print(javaflags)
            print(CMD_JAR)
            run = CMD_JAVA + javaflags + CMD_JAR
            
