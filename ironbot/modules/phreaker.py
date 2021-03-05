import asyncio
import json
import math
import os
import re
import time
from bs4 import BeautifulSoup
from requests import get
import urllib.request
from ironbot import CMD_HELP, bot
from ironbot.events import register
from telethon import events
import asyncio
from ironbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern=r"^\.hostinfo(?: |$)(\S*)")
async def _(event):
    textx = await event.get_reply_message()
    Query = event.pattern_match.group(1)
    if Query:
        pass
    elif textx:
        Query = textx.text
    else:
        await request.edit("`Pemakaian: .h2p <host>`")
        return

    url = f'http://ip-api.com/json/{Query}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,zip,lat,lon,timezone,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query'
    request = get(url)
    result = json.loads(request.text)

    if request.status_code != 200:
        await event.edit("`link Salah..`")
        return
    
    if result['status'] != 'success':
        await event.edit("```Salah Noob wkwkwk!!!\n\nCek dulu jangan make http://\nContoh : google.com```")
        return
    await event.edit(f"Hasil dari {Query}\n\n**IP** : `{result['query']}`\n**ISP** : `{result['isp']}`\n**ORG** : `{result['org']}`\n**NEGARA** : `{result['country']}`\n**KOTA** : `{result['city']}`\n**TimeZone** : `{result['timezone']}`\n\n`[STATUS : {result['status']}]` ")
    


CmdHelp('phreaker').add_command(
    'hostinfo', '<host/IP>', 'Convert host ke IP. Jangan make http:// di awalan Link , boleh makai www'
).add