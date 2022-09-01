options = {
    "name": "ZStart",
    "version": "1.1pre",
    "LibDir": "libraries",
    "CleanRoom": True,
}

modules = {
    "32Bits": True,
    "64Bits": True,
    "OneFile": False,
    "OneLib": True, # Requires EXE Wrapper
}

#https://github.com/adang1345/PythonWindows/blob/master/3.8.13
pyPaths = {
    "Py32": "C:\\Program Files (x86)\\Python38-32\\python.exe",
    "Ins32": "C:\\Program Files (x86)\\Python38-32\\Scripts\\pyinstaller.exe",
    "Py64": "C:\\Program Files\\Python38\\python.exe",
    "Ins64": "C:\\Program Files\\Python38\\Scripts\\pyinstaller.exe",
    # Add to system variables or set here
    "rar": "rar",
    "7zip": "7zip",
}

# https://www.7-zip.org/download.html
# https://www.rarlab.com/download.htm
rarFiles = {
    #"7Zip": False, [UNSUPPORTED]
    "RAR": True,
    "exclude": [
        "*.py",
        "*.pyc",
        "*.pyw",
    ],
    "include": [
        "..\\src\\resources\\config.yml",
    ]
}

#https://pyinstaller.org/en/stable/usage.html#options
pyIns = {
    "obfs-imports": [
    ],
    "script": "../src/main/Master.py",
    "imports": "../src/main",
    "output": "./product",
    "temp": "./utils/temp",
    "icon": "./utils/favicon.ico",
    "data": [
        #Windows: '--add-data=PATH;DESTINATION', Linux: "--add-data=PATH:DESTINATION"
    ],
    "hidden-imports": [
    ]
}