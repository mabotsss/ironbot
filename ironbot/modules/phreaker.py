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



@register(outgoing=True, pattern=r"^\.device(?: |$)(\S*)")
async def device_info(request):
    textx = await request.get_reply_message()
    codename = request.pattern_match.group(1)
    if codename:
        pass
    elif textx:
        codename = textx.text
    else:
        await request.edit("`Usage: .device <codename> / <model>`")
        return
    data = json.loads(
        get(
            "https://raw.githubusercontent.com/androidtrackers/"
            "certified-android-devices/master/by_device.json"
        ).text
    )
    results = data.get(codename)
    if results:
        reply = f"**Search results for {codename}**:\n\n"
        for item in results:
            reply += (
                f"**Brand**: {item['brand']}\n"
                f"**Name**: {item['name']}\n"
                f"**Model**: {item['model']}\n\n"
            )
    else:
        reply = f"`Couldn't find info about {codename}!`\n"
    await request.edit(reply)


@register(outgoing=True, pattern=r"^\.twrp(?: |$)(\S*)")
async def twrp(request):
    textx = await request.get_reply_message()
    device = request.pattern_match.group(1)
    if device:
        pass
    elif textx:
        device = textx.text.split(" ")[0]
    else:
        await request.edit("`Usage: .twrp <codename>`")
        return
    url = get(f"https://dl.twrp.me/{device}/")
    if url.status_code == 404:
        reply = f"`Couldn't find twrp downloads for {device}!`\n"
        await request.edit(reply)
        return
    page = BeautifulSoup(url.content, "lxml")
    download = page.find("table").find("tr").find("a")
    dl_link = f"https://dl.twrp.me{download['href']}"
    dl_file = download.text
    size = page.find("span", {"class": "filesize"}).text
    date = page.find("em").text.strip()
    reply = (
        f"**Latest TWRP for {device}:**\n"
        f"[{dl_file}]({dl_link}) - __{size}__\n"
        f"**Updated:** __{date}__\n"
    )
    await request.edit(reply)

@register(outgoing=True, pattern=r"^\.magisk$")
async def magisk(request):
    magisk_dict = {
        "Stable": "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/stable.json",
        "Beta": "https://raw.githubusercontent.com/topjohnwu/magisk_files/master/beta.json",
    }
    releases = "Latest Magisk Releases:\n"
    for name, release_url in magisk_dict.items():
        data = get(release_url).json()
        releases += (
            f'{name}: [ZIP v{data["magisk"]["version"]}]({data["magisk"]["link"]}) | '
            f'[APK v{data["app"]["version"]}]({data["app"]["link"]}) | '
            f'[Uninstaller]({data["uninstaller"]["link"]})\n')
    await request.edit(releases)



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