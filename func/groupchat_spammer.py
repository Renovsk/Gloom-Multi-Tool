import requests
import random
import Gloom

from time import sleep
from colorama import Fore

from func.plugins.common import SlowPrint, setTitle, getheaders, proxy

def selector(token, users):
    while True:
        try:
            response = requests.post(f'https://discordapp.com/api/v9/users/@me/channels', proxies=proxy(), headers=getheaders(token), json={"recipients": users})

            if response.status_code == 204 or response.status_code == 200:
                print(f"{Fore.BLUE}Created groupchat")
            elif response.status_code == 429:
                print(f"{Fore.YELLOW}Rate limited ({response.json()['retry_after']}ms){Fore.RESET}")
            else:
                print(f"{Fore.BLUE}Error: {response.status_code}{Fore.RESET}")
        except Exception:
            pass
        except KeyboardInterrupt:
            break
    Gloom.main()

def randomizer(token, ID):
    while True:
        users = random.sample(ID, 2)
        try:
            response = requests.post(f'https://discordapp.com/api/v9/users/@me/channels', proxies={"http": f'{proxy()}'}, headers=getheaders(token), json={"recipients": users})

            if response.status_code == 204 or response.status_code == 200:
                print(f"{Fore.BLUE}Created groupchat")
            elif response.status_code == 429:
                print(f"{Fore.YELLOW}Rate limited ({response.json()['retry_after']}ms){Fore.RESET}")
            else:
                print(f"{Fore.BLUE}Error: {response.status_code}{Fore.RESET}")
        except Exception:
            pass
        except KeyboardInterrupt:
            break
    Gloom.main()


def GcSpammer(token):
    print(f'{Fore.GREEN}[{Fore.YELLOW}>>>{Fore.GREEN}] {Fore.RESET}Do you want to choose user(s) yourself to groupchat spam or do you want to select randoms?')
    sleep(1)
    print(f'''
    {Fore.RESET}[{Fore.BLUE}1{Fore.RESET}] choose user(s) yourself
    {Fore.RESET}[{Fore.BLUE}2{Fore.RESET}] randomize the users
                        ''')
    secondchoice = int(input(
        f'{Fore.GREEN}[{Fore.CYAN}>>>{Fore.GREEN}] {Fore.RESET}Second Choice: {Fore.BLUE}'))

    if secondchoice not in [1, 2]:
        print(f'{Fore.RESET}[{Fore.BLUE}Error{Fore.RESET}] : Invalid Second Choice')
        sleep(1)
        Gloom.main()

    #if they choose to import the users manually
    if secondchoice == 1:
        setTitle(f"Creating groupchats")
        #if they choose specific users
        recipients = input(
            f'{Fore.GREEN}[{Fore.CYAN}>>>{Fore.GREEN}] {Fore.RESET}Input the users you want to create a groupchat with (separate by , id,id2,id3): {Fore.BLUE}')
        user = recipients.split(',')
        if "," not in recipients:
            print(f"\n{Fore.BLUE}You didn't have any commas (,) format is id,id2,id3")
            sleep(3)
            Gloom.main()
        SlowPrint("\"ctrl + c\" at anytime to stop\n")
        sleep(1.5)
        selector(token, user)

    #if they choose to randomize the selection
    elif secondchoice == 2:
        setTitle(f"Creating groupchats")
        IDs = []
        #Get all users to spam groupchats with
        friendIds = requests.get("https://discord.com/api/v9/users/@me/relationships", proxies={"http": f'http://{proxy()}'}, headers=getheaders(token)).json()
        for friend in friendIds:
            IDs.append(friend['id'])
        SlowPrint("\"ctrl + c\" at anytime to stop\n")
        sleep(1.5)
        randomizer(token, IDs)