import json
import urllib.request
from ironbot import CMD_HELP, bot
from ironbot.events import register
from telethon import events
import asyncio
from ironbot.cmdhelp import CmdHelp


@register(outgoing=True, pattern="^.ipscan$")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(2)
    adress = input_str
    
    token = "19e7f2b6fe27deb566140aae134dec6b"
    api = "http://api.ipstack.com/" + adress + "?access_key=" + token + "&format=1"
    
    result = urllib.request.urlopen(api).read()
    result = result.decode()

    result = json.loads(result)
    a = result["type"]
    b = result["country_code"]
    c = result["region_name"]
    d = result["city"]
    e = result["zip"]
    f = result["latitude"]
    g = result["longitude"]
    await event.edit(
        f"<b><u>Gathered Information</b></u>\n\n<b>Ip type :-</b><code>{a}</code>\n<b>Country code:- </b> <code>{b}</code>\n<b>State name :-</b><code>{c}</code>\n<b>City name :- </b><code>{d}</code>\n<b>zip :-</b><code>{e}</code>\n<b>Latitude:- </b> <code>{f}</code>\n<b>Longitude :- </b><code>{g}</code>\n",
        parse_mode="HTML",
    )
    
    
@register(outgoing=True, pattern="^.host2ip$")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(2)
    Query = input_str
    
    api = "http://ip-api.com/json/" + Query
    
    result = urllib.request.urlopen(api).read()
    result = result.decode()

    result = json.loads(result)
    a = result["query"]
    await event.edit(
        f"<b><u>Gathered Information</b></u>\n\n<b>Ip type :-</b><code>{a}</code>\n",
        parse_mode="HTML",
    )


CMD_HELP.update(
    {
        "phreaker": "**IP SCANNER**\
\n\n**Syntax : **`.scanip <ip address>`\
\n**Usage :** Gives details about the ip address."
    }
)