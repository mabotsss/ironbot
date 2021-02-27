import datetime
import asyncio
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

from ironbot.helpers import name_dl, song_dl, video_dl, yt_search

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
async def port_song(event):
    if event.fwd_from:
        return
    
    cmd = event.pattern_match.group(1)
    if len(cmd) < 1:
        await event.edit(LANG['UPLOADED_WITH']) 

    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
        
    await event.edit(LANG['SEARCHING_SPOT'])  
    dosya = os.getcwd() 
    os.system(f"spotdl --song {cmd} -f {dosya}")
    await event.edit(LANG['DOWNLOADED'])    

    l = glob.glob("*.mp3")
    if len(l) >= 1:
        await event.edit(LANG['UPLOADING'])
        await event.client.send_file(
            event.chat_id,
            l[0],
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id
        )
        await event.delete()
    else:
        await event.edit(LANG['NOT_FOUND'])   
        return 
    os.system("rm -rf *.mp3")
    subprocess.check_output("rm -rf *.mp3",shell=True)

@register(outgoing=True, pattern="^.song2(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        reply_to_id = await event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply:
        if reply.message:
            query = reply.message
    else:
        await event.edit("`What I am Supposed to find `")
        return
    iron = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    ironevent = await event.edit("`wi8..! I am finding your song....`")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await ironevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    cmd = event.pattern_match.group(1)
    if cmd == "song":
        q = "128k"
    elif cmd == "song320":
        q = "320k"
    song_cmd = song_dl.format(QUALITY="128k", video_link=video_link)
    # thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    try:
        iron = Get(iron)
        await event.client(iron)
    except BaseException:
        pass
    stderr = (await _ironutils.runcmd(song_cmd))[1]
    if stderr:
        return await ironevent.edit(f"**Error :** `{stderr}`")
    ironname, stderr = (await _ironutils.runcmd(name_cmd))[:2]
    if stderr:
        return await ironevent.edit(f"**Error :** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    ironname = os.path.splitext(ironname)[0]
    # if stderr:
    #    return await ironevent.edit(f"**Error :** `{stderr}`")
    song_file = Path(f"{ironname}.mp3")
    if not os.path.exists(song_file):
        return await ironevent.edit(
            f"Sorry!. I can't find any related video/audio for `{query}`"
        )
    await ironevent.edit("`yeah..! i found something wi8..🥰`")
    ironthumb = Path(f"{ironname}.jpg")
    if not os.path.exists(ironthumb):
        ironthumb = Path(f"{ironname}.webp")
    elif not os.path.exists(ironthumb):
        ironthumb = None

    await event.client.send_file(
        event.chat_id,
        song_file,
        force_document=False,
        caption=query,
        thumb=ironthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await ironevent.delete()
    for files in (ironthumb, song_file):
        if files and os.path.exists(files):
            os.remove(files)


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

CmdHelp('song').add_command(
    'deez', '<Judul lagu/youtube/spotify/soundcloud>', 'Cari dan unduh lagu dari banyak situs.'
).add_command(
    'song', '<Judul lagu/youtube/spotify>', 'Download lagu.'
).add_command(
    'songpl', '<spotify playlist>', 'Spotify Playlist\'mengunduh lagu dari dalam'
).add()