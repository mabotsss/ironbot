from random import randint
from asyncio import sleep
from os import execl
import sys
import io
import sys
from ironbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from ironbot.events import register
from ironbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from ironbot.language import get_value
LANG = get_value("misc")

# ████████████████████████████████ #


@register(outgoing=True, pattern="^.sleep( [0-9]+)?$")
async def sleepybot(time):
    if " " not in time.pattern_match.group(1):
        await time.reply(LANG['SLEEP_DESC'])
    else:
        counter = int(time.pattern_match.group(1))
        await time.edit(LANG['SLEEPING'])
        await sleep(2)
        if BOTLOG:
            await time.client.send_message(
                BOTLOG_CHATID,
                "Bot" + str(counter) + "detik sleep.",
            )
        await sleep(counter)
        await time.edit(LANG['GOODMORNIN_YALL'])


@register(outgoing=True, pattern="^.shutdown$")
async def shutdown(event):
    await event.client.send_file(event.chat_id, 'https://www.winhistory.de/more/winstart/mp3/winxpshutdown.mp3', caption=LANG['GOODBYE_MFRS'], voice_note=True)
    await event.delete()

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                        "Bot dimatikan.")
    try:
        await bot.disconnect()
    except:
        pass


@register(outgoing=True, pattern="^.restart$")
async def restart(event):
    await event.edit(LANG['RESTARTING'])
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                        "Bot dimulai ulang.")

    try:
        await bot.disconnect()
    except:
        pass

    execl(sys.executable, sys.executable, *sys.argv)


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    await wannasee.edit(LANG['REPO'])


CmdHelp('misc').add_command(
    'sleep', '<detik>', 'Ironbot juga manusia, dia juga mulai lelah. Biarkan dia tidur sesekali.', 'sleep 30'
).add_command(
    'shutdown', None, 'mematikan bot.'
).add_command(
    'repo', None, 'Ironbot di Github.'
).add_command(
    'restart', None, 'Restart Ironbot.'
).add()