import requests

from colorama import Fore

from func.plugins.common import getheaders, proxy

def Leaver(token, guilds):
    for guild in guilds:
        response = requests.delete(f'https://discord.com/api/v8/users/@me/guilds/'+guild['id'], proxies=proxy(), headers={'Authorization': token})
        if response.status_code == 204 or response.status_code == 200:
            #Leave servers the user is in
            print(f"{Fore.YELLOW}Left guild: {Fore.WHITE}"+guild['name']+Fore.RESET)
        elif response.status_code == 400:
            #Delete the servers the user owns
            requests.delete(f'https://discord.com/api/v8/guilds/'+guild['id'], proxies=proxy(), headers=getheaders(token))
            print(f'{Fore.BLUE}Deleted guild: {Fore.WHITE}'+guild['name']+Fore.RESET)
        else:
            print(f"The following error has been encountered and is being ignored: {response.status_code}")
            pass