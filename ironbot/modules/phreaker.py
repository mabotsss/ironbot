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
    stts = result['status']
    qry = result['query']
    bnua = result['continent']
    ngra = result['country']
    kta = result['city']
    latd = result['lat']
    lond = result['lon']
    tmzn = result['timezone']
    crncy = result['currency']
    iespe = result['isp']
    org = result['org']
    
    if result['status'] == 'success': 
        await event.edit(f"Hasil dari {Query}\n\n**IP** : `{qry}`\n**ISP** : `{iespe}`\n**NEGARA** : `{ngra}`\n**KOTA** : `{kta}`\n**BENUA** : `{bnua}`\n")
    elif result['status'] == 'fail':
        await event.edit("Salah Noob")
    




CmdHelp('notes').add_command(
    'h2p', '<link>', 'Convert host ke IP.'
).add