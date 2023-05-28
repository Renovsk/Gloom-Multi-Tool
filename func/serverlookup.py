import os
import sys
import os.path
import colorama
import requests
import webbrowser
from time import sleep
from requests.api import options
from colorama import Fore, Back, Style, init

from func.plugins.common import *

colorama.init(autoreset=True)

def menu():
    print(f"""
{Fore.BLUE}[{Fore.RESET}1{Fore.BLUE}] {Fore.RESET}Server Lookup
{Fore.BLUE}[{Fore.RESET}2{Fore.BLUE}]{Fore.RESET} Exit
""")
menu()

option = int(input(f"{Fore.BLUE}Choice?: "))

def fetch_data():
        menu()
if option == 1:
        sleep(1)

        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
            'Authorization' : input(f"{Fore.BLUE}Token:{Fore.RESET} ")
        }

        guildId = input(f"{Fore.BLUE}Server ID:{Fore.RESET} ")

        response = requests.get(
            f"https://discord.com/api/guilds/{guildId}",
            headers = headers,
            params = {"with_counts" : True}
        ).json()

        owner = requests.get(
            f"https://discord.com/api/guilds/{guildId}/members/{response['owner_id']}",
            headers = headers,
            params = {"with_counts" : True}
        ).json()

        print(f"""
{Fore.RESET}{Fore.GREEN}####### Server Infomation #######{Fore.RESET}
[{Fore.BLUE}Name{Fore.RESET}]      $:   {response['name']} 
[{Fore.BLUE}ID{Fore.RESET}]        $:   {response['id']}
[{Fore.BLUE}Owner{Fore.RESET}]     $:   {owner['user']['username']}#{owner['user']['discriminator']} 
[{Fore.BLUE}Owner ID{Fore.RESET}]  $:   {response['owner_id']}
[{Fore.BLUE}Members{Fore.RESET}]   $:   {response['approximate_member_count']}
[{Fore.BLUE}Region{Fore.RESET}]    $:   {response['region']}
[{Fore.BLUE}Icon URL{Fore.RESET}]  $:   https://cdn.discordapp.com/icons/{guildId}/{response['icon']}.webp?size=256
""")
        sleep(6)
        main()

elif option == 2:
    main()
if __name__ == '__main__':
        fetch_data()