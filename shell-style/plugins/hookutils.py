import requests
from plugins.common import *
import time

def wsend(webhook, message):
    r = requests.post(webhook, json={"content": message})
    if r.status_code == 204:
        success(fr'Message Sent ({r.status_code})')
        
    elif r.status_code == 429:
        print(f"{Fore.YELLOW}Rate limited ({r.json()['retry_after']}ms){Fore.RESET} ({r.status_code})")

def wdelete(webhook):
    r = requests.delete(webhook)
    if r.status_code == 204:
        success(f'Successfully deleted webhook! ({r.status_code})')

    elif r.status_code != 204:
        error(f'Couldn\'t delete, is the webhook valid? ({r.status_code})')
        

def wspam(webhook, message):
    while True:
        try:
            r = requests.post(webhook, json={"content": message})
            if r.status_code == 204:
                success(fr'Message Sent ({r.status_code})')

            elif r.status_code == 429:
                print(f"{Fore.YELLOW}Rate limited ({r.json()['retry_after']}ms){Fore.RESET} ({r.status_code})")
                time.sleep(r.json()["retry_after"] / 1000)
        
        except KeyboardInterrupt:
            loading('Stopping..')
            break