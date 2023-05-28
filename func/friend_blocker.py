import requests

from colorama import Fore

from func.plugins.common import getheaders, proxy

def Block(token, friends):
    #get all friends
    for friend in friends:
        try:
            #block all friends they have
            requests.put(
                f'https://discord.com/api/v9/users/@me/relationships/'+friend['id'], proxies=proxy(), headers=getheaders(token), json={"type": 2})
            print(f"{Fore.GREEN}blocked: {Fore.WHITE}"+friend['user']['username']+"#"+friend['user']['discriminator']+Fore.RESET)
        except Exception as e:
            print(f"The following error has been encountered and is being ignored: {e}")