from dataclasses import dataclass, field
from typing import Dict, List

import versions

from utils import useful

@dataclass
class ConfigData():
    config_version: str = versions.CONFIG_FORMAT
    debug_mode: bool = False

    class scripts:
        on_restart: str = ""
        on_start: str = ""
        on_stop: str = ""

    class settings:
        auto_eula: bool = True
        auto_start: bool = False
        always_restart: bool = False

        class after_stop:
            active: bool = True
            do_exit: bool = False
            pause: bool = False
            timer: int = 15

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
            file_encoding: str = "UTF-8"
            log4j2_debug: bool = False
            log4j2_configFile: str = ""

            eula_skip: bool = False
            paper_log_level: str = ""
            paper_skip_properties_comments: bool = False

    class java:
        java_binary: str = "java.exe"
        heap_unit: str = "MB"
        max_memory: int = 1024
        min_memory: int = 1024
        memory_percent = 100

    def get_exec_path(self) -> str:
        return self.server.jar_path + self.server.jar_name

    def get_jar_flags(self) -> list[str]:
        flags = []
        self.add_auto_flags(flags)
        flags.extend(useful.slith(self.server.before_jar))
        return flags

    def get_jar_args(self) -> list[str]:
        args = []
        args.extend(useful.slith(self.server.parameters))
        return args

    def get_jvm_flags(self) -> list[str]:
        flags = []
        flags.extend(useful.slith(self.java.flags.defaults))
        # TODO: Add support for flag modules
        return flags

    def get_jvm_mem(self) -> list[str]:
        xms = useful.get_percentage(self.java.min_memory, self.java.memory_percent)
        xmx = useful.get_percentage(self.java.max_memory, self.java.memory_percent)

        return [f'-Xms{xms}{self.java.heap_unit}', f'-Xmx{xmx}{self.java.heap_unit}']

    def add_auto_flags(self, flags: list) -> None:
        toggles = self.server.auto_flags
        if toggles.log4j2_debug:
            flags.append("-Dlog4j2.debug=TRUE")
        if toggles.log4j2_configFile:
            flags.append(f"-Dlog4j2.configurationFile={toggles.log4j2_configFile}")
        if toggles.file_encoding:
            flags.append(f"-Dfile.encoding={toggles.file_encoding}")

        if toggles.eula_skip:
            flags.append("-Dcom.mojang.eula.agree=TRUE")
        if toggles.paper_log_level:
            flags.append(f"-Dpaper.log-level={toggles.paper_log_level}")
        if toggles.paper_skip_properties_comments:
            flags.append("-Dpaper.skipServerPropertiesComments=TRUE")