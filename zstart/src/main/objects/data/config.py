from dataclasses import dataclass, field
from typing import Dict, List

#import versions

@dataclass
class ConfigData():
    debug_mode: bool = False
    #config_version: str = versions.CONFIG_FORMAT

    class scripts:
        on_start: str = ""
        on_stop: str = ""
        on_restart: str = ""

    class settings:
        auto_start: bool = False
        auto_eula: bool = True
        always_restart: bool = False

        class after_stop:
            active: bool = True
            pause: bool = False
            timer: int = 15
            do_exit: bool = False

    class console:
        title: str = "Minecraft Server Instance"
        background_color: str = "#0C0C0C"
        text_color: str = "#F2F2F2"

    class server:
        server_path: str = "./Server"
        jar_path: str = "./"
        jar_name: str = "server.jar"
        parameters: str | list[str] = "-nogui"
        before_jar: str | list[str] = ""

        class auto_flags:
            eula_skip: bool = False
            paper_log_level: str = "INFO"

    class java:
        java_binary: str = "java.exe"
        heap_unit: str = "MB"
        max_memory: int = 1024
        min_memory: int = 1024
        memory_percent = 100

        class flags:
            defaults: str = ""
            modules_path: str = "./flags"
            modules: list[str] = []


configData = ConfigData()