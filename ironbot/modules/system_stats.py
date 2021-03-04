from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import uname
from shutil import which
from os import remove
from ironbot import CMD_HELP, IRON_VERSION, bot, ALIVE_LOGO, ALIVE_NAME
from ironbot.events import register
from ironbot.main import PLUGIN_MESAJLAR
from telethon import version
from platform import python_version
from ironbot.cmdhelp import CmdHelp
import time
import sys
import os
import asyncio

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================

from ironbot.language import get_value
LANG = get_value("system_stats")

# ████████████████████████████████ #

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["Dtk", "Mnt", "Jam", "Hari"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

Lastupdate = time.time()
# ============================================

@register(outgoing=True, pattern="^.sysd$")
async def sysdetails(sysd):
    try:
        neo = "neofetch --stdout"
        fetch = await asyncrunapp(
            neo,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await fetch.communicate()
        result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        await sysd.edit("`" + result + "`")
    except FileNotFoundError:
        await sysd.edit(LANG['NO_NEOFETCH'])


@register(outgoing=True, pattern="^.botver$")
async def bot_ver(event):
    if which("git") is not None:
        invokever = "git describe --all --long"
        ver = await asyncrunapp(
            invokever,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await ver.communicate()
        verout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        invokerev = "git rev-list --all --count"
        rev = await asyncrunapp(
            invokerev,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        await event.edit(f"`{LANG['VERSION']}: "
                         f"{verout}"
                         "` \n"
                         f"`{LANG['REVOUT']}: "
                         f"{revout}"
                         "`")
    else:
        await event.edit(
            "Ironbots 🐺"
        )


@register(outgoing=True, pattern="^.pip(?: |$)(.*)")
async def pipcheck(pip):
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        await pip.edit(f"`{LANG['SEARCHING']} . . .`")
        invokepip = f"pip3 search {pipmodule}"
        pipc = await asyncrunapp(
            invokepip,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        if pipout:
            if len(pipout) > 4096:
                await pip.edit(LANG['BIG'])
                file = open("output.txt", "w+")
                file.write(pipout)
                file.close()
                await pip.client.send_file(
                    pip.chat_id,
                    "output.txt",
                    reply_to=pip.id,
                )
                remove("output.txt")
                return
            await pip.edit(f"**{LANG['QUERY']}: **\n`"
                           f"{invokepip}"
                           f"`\n**{LANG['RESULT']}: **\n`"
                           f"{pipout}"
                           "`")
        else:
            await pip.edit(f"**{LANG['QUERY']}: **\n`"
                           f"{invokepip}"
                           f"`\n**{LANG['RESULT']}: **\n`{LANG['NOT_FOUND']}.`")
    else:
        await pip.edit(LANG['EXAMPLE'])


@register(outgoing=True, pattern="^.alive$|^.on$")
async def ironalive(alive):
    if alive.fwd_from:
        return
    me = await alive.client.get_me()
    uptime = get_readable_time((time.time() - Lastupdate))
    await alive.get_chat()
    pm_caption = (
         "╭━━━━━━| 𝙸𝚁𝙾𝙽𝙱𝙾𝚃 |━━━━━━╮\n"
        f"┣•👤 [{me.first_name}](tg://user?id={me.id})\n"
        f"┣▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n"
        f"┣[•🤖 `Iron Ver : {IRON_VERSION} `\n"
        f"┣[•🐍 `Python.  : v.{python_version()} `\n"
        f"┣[•⚙️ `Telethon : v.{version.__version__} `\n"
        f"┣[•💡 `Base on  : master `\n"
        f"┣[•📍 `Plugin.  : {len(CMD_HELP)} `\n"
        f"┣[•🕒 `Uptime.  : {uptime} `\n"
        f"╰━━━━━━━━━━━━━━━━━━━━╯\n"         
    )
    
    await bot.send_message(
        alive.chat_id,
        pm_caption,
        reply_to=alive.message.reply_to_msg_id,
        force_document=False,
        silent=True,
    )
    await alive.delete()

@register(outgoing=True, pattern=r"^\.(?:xalive)\s?(.)?")
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    user = await bot.get_me()
    me = await alive.client.get_me()
    uptime =  get_readable_time((time.time() - Lastupdate))
    output = (
        f" **┗┓ ----IRONBOT---- ┏┛** \n"
        f"**━━━━━━━━━━━━━━━━━━━━**\n"
        f"**♛ Iron** \n"
        f" ➥ [{me.first_name}](tg://user?id={me.id}) \n"
        f"**♛ Username** \n"
        f" ➥ `@{user.username}` \n"
        f"┏━━━━━━━━━━━━━━━━━━━\n"
        f"┣[• `Telethon :`Ver {version.__version__} \n"
        f"┣[• `Python   :`Ver {python_version()} \n"
        f"┣[• `Bot Ver  :`{IRON_VERSION} \n"
        f"┣[• `Modules  :`{len(CMD_HELP)} \n"
        f"┣[• `Uptime   :`{uptime} \n"
        f"┗━━━━━━━━━━━━━━━━━━━")
    if ALIVE_LOGO:
        await bot.send_message(
            alive.chat_id,
            ALIVE_LOGO,
            output,
            reply_to=alive.message.reply_to_msg_id,
            force_document=False,
            silent=True,
        )
        await alive.delete()
    else:
        await alive.edit(output)
        await asyncio.sleep(60)
        await alive.delete()



CmdHelp('system_stats').add_command(
    'sysd', None, 'Menampilkan informasi sistem menggunakan modul Neofetch.'
).add_command(
    'botver', None, 'Menunjukkan versi ironbot.'
).add_command(
    'pip', '<modul>', 'Mencari modul pip.'
).add_command(
    'alive/on', None, 'Digunakan untuk memeriksa apakah ironbot sedang berjalan.'
).add()