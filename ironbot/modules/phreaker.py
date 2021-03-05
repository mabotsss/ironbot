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

@register(outgoing=True, pattern=r"^\.h2p(?: |$)(\S*)")
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
        await event.edit("`Invalid link.`")
        return
    
    try:
        return await event.edit(f"Hasil dari {Query}\n\n**IP** : `{result['query']}`\n**ISP** : `{result['isp']}`\n**ORG** : `{result['org']}`\n**NEGARA** : `{result['country']}`\n**KOTA** : `{result['city']}`\n**TimeZone** : `{result['timezone']}`\n")
    except Exception as e:  # pylint:disable=C0103,W0703
        return await event.edit(f"{str(type(e)): {str(e)}}")
       # await event.edit(str(e))
     #   await event.edit("Salah Noob wkwkwk!!!\nya masa make http://")
    




CmdHelp('notes').add_command(
    'h2p', '<link>', 'Convert host ke IP.'
).add