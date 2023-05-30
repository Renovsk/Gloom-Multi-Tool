import os
import re
import io
import sys
import time
import json
import shutil
import ctypes
import random
import zipfile
import requests
import threading
import subprocess
import pylibcheck

from urllib.request import urlopen, urlretrieve
from distutils.version import LooseVersion
from bs4 import BeautifulSoup
from colorama import Fore
from time import sleep

THIS_VERSION = "1.3.0"

google_target_ver = 0
edge_target_ver = 0

class Chrome_Installer(object):
    installed = False
    target_version = None
    DL_BASE = "https://chromedriver.storage.googleapis.com/index.html?path=109.0.5414.25/"

    def __init__(self, executable_path=None, target_version=None, *args, **kwargs):
        self.platform = sys.platform

        if google_target_ver:
            self.target_version = google_target_ver

        if target_version:
            self.target_version = target_version

        if not self.target_version:
            self.target_version = self.get_release_version_number().version[0]

        self._base = base_ = "chromedriver{}"

        exe_name = self._base
        if self.platform in ("win32",):
            exe_name = base_.format(".exe")
        if self.platform in ("linux",):
            self.platform += "64"
            exe_name = exe_name.format("")
        if self.platform in ("darwin",):
            self.platform = "mac64"
            exe_name = exe_name.format("")
        self.executable_path = executable_path or exe_name
        self._exe_name = exe_name

        if not os.path.exists(self.executable_path):
            self.fetch_chromedriver()
            if not self.__class__.installed:
                if self.patch_binary():
                    self.__class__.installed = True

    @staticmethod
    def random_cdc():
        cdc = random.choices('abcdefghijklmnopqrstuvwxyz', k=26)
        cdc[-6:-4] = map(str.upper, cdc[-6:-4])
        cdc[2] = cdc[0]
        cdc[3] = "_"
        return "".join(cdc).encode()

    def patch_binary(self):
        linect = 0
        replacement = self.random_cdc()
        with io.open(self.executable_path, "r+b") as fh:
            for line in iter(lambda: fh.readline(), b""):
                if b"cdc_" in line:
                    fh.seek(-len(line), 1)
                    newline = re.sub(b"cdc_.{22}", replacement, line)
                    fh.write(newline)
                    linect += 1
            return linect

    def get_release_version_number(self):
        path = (
            "LATEST_RELEASE"
            if not self.target_version
            else f"LATEST_RELEASE_{self.target_version}"
        )
        return LooseVersion(urlopen(self.__class__.DL_BASE + path).read().decode())

    def fetch_chromedriver(self):
        base_ = self._base
        zip_name = base_.format(".zip")
        ver = self.get_release_version_number().vstring
        if os.path.exists(self.executable_path):
            return self.executable_path
        urlretrieve(
            f"{self.__class__.DL_BASE}{ver}/{base_.format(f'_{self.platform}')}.zip",
            filename=zip_name,
        )
        with zipfile.ZipFile(zip_name) as zf:
            zf.extract(self._exe_name)
        os.remove(zip_name)
        if sys.platform != "win32":
            os.chmod(self._exe_name, 0o755)
        return self._exe_name

class Edge_Installer(object):
    installed = False
    target_version = None
    DL_BASE = "https://msedgedriver.azureedge.net/"

    def __init__(self, executable_path=None, target_version=None, *args, **kwargs):
        self.platform = sys.platform

        if edge_target_ver:
            self.target_version = edge_target_ver

        if target_version:
            self.target_version = target_version

        if not self.target_version:
            self.target_version = self.get_release_version_number().version[0]

        self._base = base_ = "edgedriver{}"

        exe_name = self._base
        if self.platform in ("win32",):
            exe_name = base_.format(".exe")
        if self.platform in ("linux",):
            self.platform += "64"
            exe_name = exe_name.format("")
        if self.platform in ("darwin",):
            self.platform = "mac64"
            exe_name = exe_name.format("")
        self.executable_path = executable_path or exe_name
        self._exe_name = exe_name

        if not os.path.exists(self.executable_path):
            self.fetch_edgedriver()
            if not self.__class__.installed:
                if self.patch_binary():
                    self.__class__.installed = True

    @staticmethod
    def random_cdc():
        cdc = random.choices('abcdefghijklmnopqrstuvwxyz', k=26)
        cdc[-6:-4] = map(str.upper, cdc[-6:-4])
        cdc[2] = cdc[0]
        cdc[3] = "_"
        return "".join(cdc).encode()

    def patch_binary(self):
        linect = 0
        replacement = self.random_cdc()
        with io.open("ms"+self.executable_path, "r+b") as fh:
            for line in iter(lambda: fh.readline(), b""):
                if b"cdc_" in line:
                    fh.seek(-len(line), 1)
                    newline = re.sub(b"cdc_.{22}", replacement, line)
                    fh.write(newline)
                    linect += 1
            return linect


    def get_release_version_number(self):
        path = (
            "LATEST_STABLE"
            if not self.target_version
            else f"LATEST_RELEASE_{str(self.target_version).split('.', 1)[0]}"
        )
        urlretrieve(
            f"{self.__class__.DL_BASE}{path}",
            filename=f"{getTempDir()}\\{path}",
        )
        with open(f"{getTempDir()}\\{path}", "r+") as f:
            _file = f.read().strip("\n")
            content = ""
            for char in [x for x in _file]:
                for num in ("0","1","2","3","4","5","6","7","8","9","."):
                    if char == num:
                        content += char
        return LooseVersion(content)

    def fetch_edgedriver(self):
        base_ = self._base
        zip_name = base_.format(".zip")
        ver = self.get_release_version_number().vstring
        if os.path.exists(self.executable_path):
            return self.executable_path
        urlretrieve(
            f"{self.__class__.DL_BASE}{ver}/{base_.format(f'_{self.platform}')}.zip",
            filename=zip_name,
        )
        with zipfile.ZipFile(zip_name) as zf:
            zf.extract("ms"+self._exe_name)
        os.remove(zip_name)
        if sys.platform != "win32":
            os.chmod(self._exe_name, 0o755)
        return self._exe_name

class Opera_Installer(object):
    DL_BASE = "https://github.com"
    def __init__(self, *args, **kwargs):
        self.platform = sys.platform
        self.links = ""

        r = requests.get(self.__class__.DL_BASE+"/operasoftware/operachromiumdriver/releases")
        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('a'):
            if "operadriver" in link.get('href'):
                self.links += f"{link.get('href')}\n"

        for i in self.links.split("\n")[:4]:
            if self.platform in i:
                self.fetch_edgedriver(i)

    def fetch_edgedriver(self, driver):
        executable = "operadriver.exe"
        driver_name = driver.split("/")[-1]
        cwd = os.getcwd() + os.sep

        urlretrieve(self.__class__.DL_BASE+driver, filename=driver_name)
        with zipfile.ZipFile(driver_name) as zf:
            zf.extractall()
        shutil.move(cwd+driver_name[:-4]+os.sep+executable, cwd+executable)
        os.remove(driver_name)
        shutil.rmtree(driver_name[:-4])

def getDriver():
    #supported drivers
    drivers = ["chromedriver.exe", "msedgedriver.exe", "operadriver.exe"]
    print(f"\n{Fore.BLUE}Checking Driver. . .")
    sleep(0.5)

    for driver in drivers:
        #Checking if driver already exists
        if os.path.exists(os.getcwd() + os.sep + driver):
            print(f"{Fore.GREEN}{driver} already exists, continuing. . .{Fore.RESET}")
            sleep(0.5)
            return driver
    else:
        print(f"{Fore.RED}Driver not found! Installing it for you")
        #get installed browsers + install driver + return correct driver
        if os.path.exists(os.getenv('localappdata') + '\\Google'):
            Chrome_Installer()
            print(f"{Fore.GREEN}chromedriver.exe Installed!{Fore.RESET}")
            return "chromedriver.exe"
        elif os.path.exists(os.getenv('appdata') + '\\Opera Software\\Opera Stable'):
            Opera_Installer()
            print(f"{Fore.GREEN}operadriver.exe Installed!{Fore.RESET}")
            return "operadriver.exe"
        elif os.path.exists(os.getenv('localappdata') + '\\Microsoft\\Edge'):
            Edge_Installer()
            print(f"{Fore.GREEN}msedgedriver.exe Installed!{Fore.RESET}")
            return "msedgedriver.exe"
        else:
            print(f'{Fore.RESET}[{Fore.RED}Error{Fore.RESET}] : No compatible driver found. . . Proceeding with chromedriver')
            Chrome_Installer()
            print(f"{Fore.GREEN}trying with chromedriver.exe{Fore.RESET}")
            return "chromedriver.exe"

def clear():
    system = os.name
    if system == 'nt':
        #if its windows
        os.system('cls')
    elif system == 'posix':
        #if its linux
        os.system('clear')
    else:
        print('\n'*120)
    return

def setTitle(_str):
    system = os.name
    if system == 'nt':
        #if its windows
        ctypes.windll.kernel32.SetConsoleTitleW(f"Gloom 1.3.0 @ Menu")
    elif system == 'posix':
        #if its linux
        sys.stdout.write(f"Gloom 1.3.0 @ Menu")
    else:
        #if its something else or some err happend for some reason, we do nothing
        pass

def getTempDir():
    system = os.name
    if system == 'nt':
        #if its windows
        return os.getenv('temp')
    elif system == 'posix':
        #if its linux
        return '/tmp/'

def RandomChinese(amount, second_amount):
    name = u''
    for i in range(random.randint(amount, second_amount)):
        name = name + chr(random.randint(0x4E00,0x8000))
    return name

def SlowPrint(_str):
    for letter in _str:
        #slowly print out the words 
        sys.stdout.write(letter);sys.stdout.flush();sleep(0.04)

def installPackage(dependencies):
    print(f'{Fore.CYAN}Checking packages. . .{Fore.RESET}')
    if sys.argv[0].endswith('.exe'):
            #get all installed libs
            reqs = subprocess.check_output(['python', '-m', 'pip', 'freeze'])
            installed_packages = [r.decode().split('==')[0].lower() for r in reqs.split()]

            for lib in dependencies:
                #check for missing libs 
                if lib not in installed_packages:
                    #install the lib if it wasn't found
                    print(f"{Fore.BLUE}{lib}{Fore.RED} not found! Installing it for you. . .{Fore.RESET}")
                    try:
                        subprocess.check_call(['python', '-m', 'pip', 'install', lib])
                    #incase something goes wrong we notify the user that something happend
                    except Exception as e:
                        print(f"{Fore.RESET}[{Fore.RED}Error{Fore.RESET}] : {e}")
                        sleep(0.5)
                        pass
    else:
        for i in dependencies:
            if not pylibcheck.checkPackage(i):
                print(f"{Fore.BLUE}{i}{Fore.RED} not found! Installing it for you. . .{Fore.RESET}")
                pylibcheck.installPackage(i)

def hasNitroBoost(token):
    '''return True if they got nitro boost and False if they don't'''
    channelIds = requests.get("https://discordapp.com/api/v9/users/@me/billing/subscriptions", headers=getheaders(token)).json()
    try:
        if channelIds[0]["type"] == 1:
            return True
    except Exception:
        return False

def validateToken(token):
    '''validate the token by contacting the discord api'''
    #define variables
    base_url = "https://discord.com/api/v9/users/@me"
    message = "You need to verify your account in order to perform this action."
    #contact discord api and see if you can get a valid response with the given token
    r = requests.get(base_url, headers=getheaders(token))
    if r.status_code != 200:
        #invalid token
        print(f"\n{Fore.RED}Invalid Token.{Fore.RESET}")
        sleep(1)
        __import__("Gloom").main()
    j = requests.get(f'{base_url}/billing/subscriptions', headers=getheaders(token)).json()
    #check if the account is phone locked
    try:
        if j["message"] == message:
            print(f"\n{Fore.RED}Phone Locked Token.{Fore.RESET}")
            sleep(1)
            __import__("Gloom").main()
    except (KeyError, TypeError, IndexError):
        pass

def validateWebhook(hook):
    #if the input is something like google.com or something else we check if it contains api/webhooks first
    if not "api/webhooks" in hook:
        print(f"\n{Fore.RED}Invalid Webhook.{Fore.RESET}")
        sleep(1)
        __import__("Gloom").main()
    try:
        #try and get a connection with the input
        responce = requests.get(hook)
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema, requests.exceptions.ConnectionError):
        #connection failed
        print(f"\n{Fore.RED}Invalid Webhook.{Fore.RESET}")
        sleep(1)
        __import__("Gloom").main()
    try:
        #try and get a value from object
        j = responce.json()["name"]
    except (KeyError, json.decoder.JSONDecodeError):
        #if its a valid link but link isn't a webhook
        print(f"\n{Fore.RED}Invalid Webhook.{Fore.RESET}")
        sleep(1)
        __import__("Gloom").main()
    #webhook is valid
    print(f"{Fore.GREEN}Valid webhook! ({j})")


def proxy_scrape():
    setTitle("Loading Proxies from file by ab5 best @ Gloom 1.3.0")
    print(f'''{Fore.BLUE}  __                       __   _                                                      _                
 [  |                     |  ] (_)                                                    (_)               
 | |   .--.   ,--.    .--.| |  __   _ .--.   .--./)  _ .--.   _ .--.   .--.   _   __  __  .---.  .--.   
 | | / .'`\ \`'_\ : / /'`\' | [  | [ `.-. | / /'`\; [ '/'`\ \[ `/'`\]/ .'`\ \[ \ [  ][  |/ /__\\( (`\]  
 | || \__. |// | |,| \__/  |  | |  | | | | \ \._//  | \__/ | | |    | \__. | > '  <  | || \__., `'.'.  
 [___]'.__.' \'-;__/ '.__.;__][___][___||__].',__`   | ;.__/ [___]    '.__.' [__]`\_][___]'.__.'[\__) ) 
                                           ( ( __)) [__|                                                {Fore.RESET}

    ''')
    global proxies
    with open("./proxies.txt", 'r') as file:
        proxies = file.readlines()
    if not proxies:
        proxies = None
    else:
        proxies = [proxy.strip() for proxy in proxies]
    
    

def proxy():
    global proxies
    if proxies is None:
        return None
    p = random.choice(proxies)
    return {'http': f'http://{p}', 'https': f'https://{p}'}
    

#headers for optimazation
heads = [
    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    },

    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/76.0"
    },

    {
       "Content-Type": "application/json",
       "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
]

def getheaders(token=None):
    headers = random.choice(heads)
    if token:
        headers.update({"Authorization": token})
    return headers

