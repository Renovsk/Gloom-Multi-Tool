import requests

from colorama import Fore
from func.plugins.common import setTitle, proxy

def MassDM(token, channels, Message):
    for channel in channels:
        for user in [x["username"]+"#"+x["discriminator"] for x in channel["recipients"]]:
            try:
                setTitle(f"Messaging "+user)
                requests.post(f'https://discord.com/api/v9/channels/'+channel['id']+'/messages',
                    proxies=proxy(),
                    headers={'Authorization': token},
                    data={"content": f"{Message}"})
                print(f"{Fore.BLUE}Messaged: {Fore.WHITE}"+user+Fore.RESET)
            except Exception as e:
                print(f"The following error has been encountered and is being ignored: {e}")