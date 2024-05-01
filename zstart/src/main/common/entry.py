import os, sys, re
from pathlib import Path

from common.colors import wc, fg, bg, ef, rs

# 7-bit C1 ANSI sequences
ANSI_ESCAPE_ALL = re.compile(r'\x1B (?:[@-Z\\-_] | \[ [0-?]* [-/]* [@-~])', re.VERBOSE)

def clear(new_line=True):
    if sys.stdin and sys.stdin.isatty():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    if new_line:
        write()

def write(*values: object, reset: bool = True, sep: str = " ", end: str = "\n"):
    print(*values, sep=sep, end=end)
    if reset:
        print(rs.all, end='')

def set_title(text: str = ""):
    if os.name == 'nt':
        import ctypes
        try:
            k32 = ctypes.WinDLL('kernel32', use_last_error=True)
            k32.SetConsoleTitleW(text)
            k32.SetConsoleMode(k32.GetStdHandle(-11), 7)
        except (WindowsError, IOError, RuntimeError):
            ctypes.WinError(ctypes.get_last_error())
            os.system(f'title {text}')
        os.system('color')
    else:
        sys.stdout.write(b'\33]0;' + text + b'\a')
        sys.stdout.flush()
        os.system('')

def load_icon(ICON_PATH):
    """Loads an icon from a file and sets it for the console window."""
    if os.name == 'nt':
        from ctypes import windll, create_unicode_buffer
        kernel32, user32 = windll.kernel32, windll.user32

        image_path = Path(ICON_PATH).absolute()

        try:
            if not image_path.exists():
                raise FileNotFoundError("Icon file does not exist")
            # Get the console window handle
            consoleTitle = create_unicode_buffer(256)
            kernel32.GetConsoleTitleW(consoleTitle, 256)
            apphWnd = user32.FindWindowW(None, consoleTitle)

            # Set icon loading flags
            icon_flags = user32.LR_LOADFROMFILE | user32.LR_DEFAULTSIZE

            # Attempt to load the icon
            hIcon = user32.LoadImageW(None, str(image_path), 1, 0, 0, icon_flags)
            user32.SendMessageA(apphWnd, user32.WM_SETICON, 0, hIcon) # Small icon
            user32.SendMessageA(apphWnd, user32.WM_SETICON, 1, hIcon) # Large icon
        except (WindowsError, IOError, RuntimeError, FileNotFoundError) as e:
            write(f"Error setting console icon: {e}")
            write(f"Path: {ICON_PATH}")

def error_message(message: str):
    write(
    """
    [WARN] {msg}
    """
    )

def get_exceptionDesc(e: Exception):
    msg = f"{e.__class__.__name__} from <'{e.__class__.__module__}'>"
    if len(e.args) > 0:
        msg += f": {e.args[0]}"


def handle_exception(e: Exception, output: str = "CONSOLE", trace: bool = True):
    import traceback
    from utils.libs import unique_handler

    if not isinstance(e, Exception): return

    content = f"""{'‾' * 45}
    [WARNING] Something awful happened!

        [INFO] {get_exceptionDesc(e)}

    """
    output = output.upper()

    if output in ("CONSOLE", "BOTH"):
        write(content)
        if trace:
            write(f"{traceback.format_exc()}")
        write('‾' * 45)

    if output in ("FILE", "BOTH"):
        file_path = unique_handler.UniqueFileManager("logs/crash-reports/", "crash", ".log", max_files=instances.configData.maxFiles["crash"]).obtain_unique_file()
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(ANSI_ESCAPE_ALL.sub('', content))
            f.write(traceback.format_exc())