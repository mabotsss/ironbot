import sys
import asyncio
import os
import re
import requests
from asyncio import create_subprocess_shell as asyncsubshell
from asyncio import subprocess as asyncsub
from os import remove
from time import gmtime, strftime
from traceback import format_exc

from telethon import events

from ironbot import bot, BOTLOG_CHATID, LOGSPAMMER, PATTERNS, SUDO_USER


def register(**args):
    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)
    groups_only = args.get('groups_only', False)
    trigger_on_fwd = args.get('trigger_on_fwd', False)
    trigger_on_inline = args.get('trigger_on_inline', False)
    disable_errors = args.get('disable_errors', False)

    if pattern:
        args["pattern"] = pattern.replace("^.", "^["+ PATTERNS + "]")
    if "disable_edited" in args:
        del args['disable_edited']

    if "ignore_unsafe" in args:
        del args['ignore_unsafe']

    if "groups_only" in args:
        del args['groups_only']

    if "disable_errors" in args:
        del args['disable_errors']

    if "trigger_on_fwd" in args:
        del args['trigger_on_fwd']
      
    if "trigger_on_inline" in args:
        del args['trigger_on_inline']

    def decorator(func):
        async def wrapper(check):
            if not LOGSPAMMER:
                send_to = check.chat_id
            else:
                send_to = BOTLOG_CHATID

            if not trigger_on_fwd and check.fwd_from:
                return

            if check.via_bot_id and not trigger_on_inline:
                return
             
            if groups_only and not check.is_group:
                await check.respond("`Saya tidak berpikir ini adalah sebuah group.`")
                return

            try:
                await func(check)
                

            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException:
                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    text = "**USERBOT LAPORAN KESALAHAN**\n"
                    link = "[Dev Ironbot](https://t.me/ndourbae)"
                    text += "`Anda dapat melaporkan ini"
                    text += f" di sini` {link}.\n"
                    
                    ftext = "--------USERBOT LAPORAN ERROR--------\n"
                    ftext += "\nTanggal: " + date
                    ftext += "\nGrup ID: " + str(check.chat_id)
                    ftext += "\nID pengirim: " + str(check.sender_id)
                    ftext += "\n\nKarena:\n"
                    ftext += str(check.text)
                    ftext += "\n\nInformasi kerusakan:\n"
                    ftext += str(format_exc())
                    ftext += "\n\nLaporan teks:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n-----USERBOT-----"

                    command = "git log --pretty=format:\"%an: %s\" -10"

                    ftext += "\n\n\nSon 10 commit:\n"

                    process = await asyncsubshell(command,
                                                  stdout=asyncsub.PIPE,
                                                  stderr=asyncsub.PIPE)
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) \
                        + str(stderr.decode().strip())

                    ftext += result

                    file = open("error.log", "w+")
                    file.write(ftext)
                    file.close()

                    if LOGSPAMMER:
                        await check.client.respond("`Maaf UserBot saya macet.\
                        \nLog kegagalan disimpan di grup log UserBot.`")

                    await check.client.send_file(send_to,
                                                 "error.log",
                                                 caption=text)
                    remove("error.log")
            else:
                pass
        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))

        return wrapper

    return decorator



# https://t.me/c/1220993104/623253
# https://docs.telethon.dev/en/latest/misc/changelog.html#breaking-changes
