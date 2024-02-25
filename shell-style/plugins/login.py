import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from colorama import Fore
from plugins.common import *
import requests

def TokenLogin(token):
    try:
        j = requests.get("https://discord.com/api/v9/users/@me", headers={'Authorization': token, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'}).json()
        user = j["username"] + "#" + str(j["discriminator"])
        
        script = """
                document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"%s"`
                location.reload();
            """ % (token)

        loading(f"{white}Logging into {blue}{user}")

        try:

            opts = webdriver.EdgeOptions()
            opts.add_experimental_option('excludeSwitches', ['enable-logging'])
            opts.add_experimental_option("detach", True)
            driver = webdriver.Edge(options=opts)
            driver.get("https://discordapp.com/login")
            driver.execute_script(script)
            success(fr'Logged in! {user}')

        except Exception as e:
            error(f"{Fore.WHITE}{e}")

    except Exception as e:
        error(fr'{red}Invalid Token {j}')
