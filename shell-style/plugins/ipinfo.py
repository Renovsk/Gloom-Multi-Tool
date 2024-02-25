import requests
from plugins.common import *

def getip(ip):
    r = requests.get(fr'https://ipinfo.io/{ip}/json').json()
    city = r['city']
    region = r['region']
    country = r['country']
    location = r['loc']
    org = r['org']
    timezone = r['timezone']
    print(fr'''
{blue}City:{white} {city}
{blue}Region:{white} {region}
{blue}Country:{white} {country}
{blue}Location:{white} {location}
{blue}Timezone:{white} {timezone}
{blue}Org:{white} {org}''')
