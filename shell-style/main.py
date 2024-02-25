from plugins import *
from plugins.common import *
from colorama import *
import os

logo = fr"""{blue} 
   _____ _                       
  / ____| |                      
 | |  __| | ___   ___  _ __ ___  
 | | |_ | |/ _ \ / _ \| '_ ` _ \ 
 | |__| | | (_) | (_) | | | | | |
  \_____|_|\___/ \___/|_| |_| |_|
    {white}coded by github.com/Renovsk"""


os.system('cls')

def menu():
    print(logo)
    while True:
      try:
        ans = input(f'\n{blue}${white} ')
        if ans.lower().startswith('login'):
          try:
            token = ans.split(' ', 1)[1]
            TokenLogin(token)

          except IndexError:
            error('login <token>')
        
        elif ans.lower().startswith('wdelete'):
          try:
            fr = ans.split(' ', 1)
            webhook = fr[1]
            wdelete(webhook)
          except IndexError:
            error('wdelete <webhook>')

        elif ans.lower().startswith('wsend'):
          try:
            fr = ans.split(' ', 2)
            webhook = fr[1]
            msg = fr[2]
            wsend(webhook, msg)

          except IndexError:
            error('wsend <webhook> <message>')

        elif ans.lower().startswith('wspam'):
          try:
            fr = ans.split(' ', 2)
            webhook = fr[1]
            msg = fr[2]
            wspam(webhook, msg)

          except IndexError:
            error('wspam <webhook> <message>')
        
        elif ans.lower().startswith('ipinfo'):
          try:
            ip = ans.split(' ', 1)[1]
            getip(ip)

          except IndexError:
            error('ip <ip>')

        elif ans.lower().startswith('help'):
          help()

        elif ans.lower().startswith('cls') or ans.lower().startswith('clear'):
          os.system('cls')
          print(logo)

        else:
          print('Invalid Command, do \"help\" to get the list of commands.')
            
      except KeyboardInterrupt:
        print(f'{red}\nExiting..')
        quit()
    # success('hey')
    # error('hey')
    # loading('hey')

menu()