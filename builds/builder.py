import os, shutil, subprocess
from sty import *
from utils.funcs import *
import config

def title():
    title = f"pyBuilder v2.0"
    if os.name == 'nt':
        import ctypes
        try:
            k32 = ctypes.WinDLL('kernel32', use_last_error=True)
            k32.SetConsoleTitleW(title)
            k32.SetConsoleMode(k32.GetStdHandle(-11), 7)
        except (WindowsError, IOError, RuntimeError):
            ctypes.WinError(ctypes.get_last_error())
            os.system(f'title {title}')
        os.system('color')
    else:
        sys.stdout.write(b'\33]0;' + title + b'\a')
        sys.stdout.flush()
        os.system("")

def cReload():
    import importlib
    importlib.reload(config)
    main()

def main():
    clear()
    if config.modules["32Bits"]:
        if not os.path.isfile(f'{config.pyPaths["Ins32"]}'):
            warn("[WARN] Pyinstaller (x32) wasn't found:")
            log(f'  "{config.pyPaths["Py32"]}" -m pip install pyinstaller\n')
            config.modules["32Bits"] = False
    if config.modules["64Bits"]:
        if not os.path.isfile(f'{config.pyPaths["Ins64"]}'):
            warn("[WARN] Pyinstaller (x64) wasn't found: ")
            log(f'  "{config.pyPaths["Py64"]}" -m pip install pyinstaller\n')
            config.modules["64Bits"] = False
    while True:
        print(f'{fg(160,85,212)}Version: {config.options["version"]}')
        print()
        print(f"{fg.magenta}-----<< {fg(240,210,40)}OPTIONS {fg.magenta}>>-----{fg.rs}")
        mPrint("[1].", f"{fg(27)}EXECompiler")
        mPrint("[2].", f"{fg(166)}RARCompress")
        print()
        mPrint("[0].", f"{fg.li_red}[EXIT]")
        print()
        action = xinput()
        if action == "0":
            return
        elif action == "1":
            build()
        elif action == "2":
            rar()
            rar(x86=True)
        elif action == "/reload":
            cReload()
        else:
            elseval()

def build():
    if not (config.modules["32Bits"] or config.modules["64Bits"]):
        warn("[WARN] Enable a build architecture first\n")
        return
    else:
        fullname = f'{config.options["name"]} v{config.options["version"]}'
        product = f'{config.pyIns["output"]}/{fullname}'
        code = []
        if config.modules["OneFile"]:
            code.append("--OneFile")
        for i in config.pyIns["hidden-imports"] + config.pyIns["obfs-imports"]:
            code.append(f"--hidden-import={i}")
        code.extend(['--clean', f'--icon={config.pyIns["icon"]}', f'--workpath={config.pyIns["temp"]}', f'--distpath={config.pyIns["output"]}', f'--paths={config.pyIns["imports"]}', *config.pyIns["data"]])
    try:
        if config.modules["32Bits"]:
            print(fg.li_blue, end='')
            print("╔==============================╗")
            print("│      Building 32Bits...      │")
            print("╚==============================╝")
            print(fg.cyan)
            subprocess.run([f'{config.pyPaths["Ins32"]}', f'--name={fullname}_x86', *code, config.pyIns["script"]])
            if config.modules["OneLib"] and not config.modules["OneFile"]:
                if os.path.isfile(f'{product}_x86/{fullname}_x86.exe'):
                    os.rename(f'{product}_x86/{fullname}_x86.exe', f'{product}_x86/{config.options["name"]}.exe')
                if not os.path.isdir(f'{product}_x86/{config.options["LibDir"]}'):
                    os.mkdir(f'{product}_x86/{config.options["LibDir"]}')
                files = [f.name for f in os.scandir(f'{product}_x86') if f.name.endswith((".pyd",".zip",".dll")) or f.name == f'{config.options["name"]}.exe' or f.is_dir() and f.name != config.options["LibDir"]]
                for i in files:
                    shutil.move(f'{product}_x86/{i}',f'{product}_x86/{config.options["LibDir"]}/{i}')
                if os.path.isfile("utils/wrapper/ZStart5.exe"):
                    shutil.copy("utils/wrapper/ZStart5.exe", f'{product}_x86')
            print(fg.rs)
        if config.modules["64Bits"]:
            print(fg.li_blue, end='')
            print("╔==============================╗")
            print("│      Building 64Bits...      │")
            print("╚==============================╝")
            print(fg.cyan)
            subprocess.run([f'{config.pyPaths["Ins64"]}', f'--name={fullname}', *code, config.pyIns["script"]])
            if config.modules["OneLib"] and not config.modules["OneFile"]:
                if os.path.isfile(f'{product}/{fullname}.exe'):
                    os.rename(f'{product}/{fullname}.exe', f'{product}/{config.options["name"]}.exe')
                if not os.path.isdir(f'{product}/{config.options["LibDir"]}'):
                    os.mkdir(f'{product}/{config.options["LibDir"]}')
                files = [f.name for f in os.scandir(product) if f.name.endswith((".pyd",".zip",".dll")) or f.name == f'{config.options["name"]}.exe' or f.is_dir() and f.name != config.options["LibDir"]]
                for i in files:
                    shutil.move(f'{product}/{i}',f'{product}/{config.options["LibDir"]}/{i}')
                if os.path.isfile("utils/wrapper/ZStart5.exe"):
                    shutil.copy("utils/wrapper/ZStart5.exe", f'{product}')
            print(fg.rs)
        if config.options["CleanRoom"]:
            if os.path.isfile(f"{fullname}_x86.spec"):
                os.remove(f"{fullname}_x86.spec")
            if os.path.isfile(f"{fullname}.spec"):
                os.remove(f"{fullname}.spec")
            if os.path.isdir(config.pyIns["temp"]):
                shutil.rmtree(config.pyIns["temp"])
    except Exception as e:
        warn(f"{e}\n")

def rar(x86=False):
    if not os.path.isdir("dist"):
        os.mkdir("dist")
    fullname = f'{config.options["name"]} v{config.options["version"]}'
    excluded = list(f"-x{i}" for i in config.rarFiles["exclude"])
    if x86:
        fullname += "_x86"
    product = f'{config.pyIns["output"]}/{fullname}'
    #if config.rarFiles["7Zip"]:
    #    cmd = [config.pyPaths["7zip"], "a"]
    if config.rarFiles["RAR"]:
        cmd = [config.pyPaths["rar"], "a", "-ep1", "-r", *excluded]
    if os.path.isfile(f"dist/{fullname}.rar"):
        os.remove(f"dist/{fullname}.rar")
    try:
        print(fg(166), end='')
        print("╔=======================╗")
        print("│      RARCompress      │")
        print("╚=======================╝")
        print(fg.yellow)
        if os.path.isfile(f'{product}.exe'):
            subprocess.run([*cmd, f"dist/{fullname}.rar", f'{product}.exe', *config.rarFiles["include"]])
        elif os.path.isfile(f'{product}/ZStart5.exe') and os.path.isdir(f'{product}/{config.options["LibDir"]}'):
            subprocess.run([*cmd, f"dist/{fullname}.rar", f'{product}/ZStart5.exe', f'{product}/{config.options["LibDir"]}', *config.rarFiles["include"]])
        print(fg.rs)
    except Exception as e:
        warn(f"{e}\n")


if __name__ == "__main__":
    title()
    main()