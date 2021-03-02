import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from ironbot.events import register
from ironbot import bot, CMD_HELP
from time import sleep
import os
from telethon.tl.types import MessageMediaPhoto
import asyncio
from ironbot.modules.admin import get_user_from_event
from PIL import Image, ImageDraw, ImageFont
import textwrap
from ironbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from ironbot.language import get_value
LANG = get_value("scrapers_bot")

# ████████████████████████████████


@register(outgoing=True, pattern="^.q(?: |$)(.*)")
async def quotly(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    chat = "@QuotLyBot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    await event.edit(LANG['QUOTING'])

    async with bot.conversation(chat, exclusive=False, replies_are_responses=True) as conv:
        response = None
        try:
            sayi = event.pattern_match.group(1)
            if len(sayi) == 1:
                sayi = int(sayi)
                i = 1
                mesajlar = [event.reply_to_msg_id]
                while i < sayi:
                    mesajlar.append(event.reply_to_msg_id + i)
                    i += 1
                msg = await event.client.forward_messages(chat, mesajlar, from_peer=event.chat_id)
            else:
                msg = await reply_message.forward_to(chat)
            response = await conv.wait_event(events.NewMessage(incoming=True,from_users=1031952739), timeout=10)
        except YouBlockedUserError: 
            await event.edit(LANG['UNBLOCK_QUOTLY'])
            return
        except asyncio.TimeoutError:
            await event.edit("`tidak ada respon, kayak doi!`")
            return
        except ValueError:
            await event.edit(LANG['QUOTLY_VALUE_ERR'])
            return
            
        if not response:
            await event.edit("`tidak ada respon, kayak doi!`")
        elif response.text.startswith("haloooo!"):
            await event.edit(LANG['USER_PRIVACY'])
        else: 
            await event.delete()
            await response.forward_to(event.chat_id)
        await conv.mark_read()
        await conv.cancel_all()

CmdHelp('quotly').add_command(
    'q', '<balas ke user>', 'Ubah teks Anda menjadi stiker.'
).add()
