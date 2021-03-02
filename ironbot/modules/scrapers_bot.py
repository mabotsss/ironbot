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

def is_message_image(message):
    if message.media:
        if isinstance(message.media, MessageMediaPhoto):
            return True
        if message.media.document:
            if message.media.document.mime_type.split("/")[0] == "image":
                return True
        return False
    return False
    
async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response

def MemeYap (Resim, Text, FontS = 40, Bottom = False, BottomText = None):
    Foto = Image.open(Resim)
    Yazi = ImageDraw.Draw(Foto)
    FontSize = 20
    ImgFraction = float(f"0.{FontS}")

    Font = ImageFont.truetype("./ironbot/fonts/impact.ttf", FontSize)
    while Font.getsize(Text)[0] < ImgFraction*Foto.size[0]:
        FontSize += 1
        Font = ImageFont.truetype("./ironbot/fonts/impact.ttf", FontSize)
    FontSize -= 1
    Font = ImageFont.truetype("./ironbot/fonts/impact.ttf", FontSize)

    def drawTextWithOutline(text, x, y):
        Yazi.text((x-2, y-2), text,(0,0,0),font=Font)
        Yazi.text((x+2, y-2), text,(0,0,0),font=Font)
        Yazi.text((x+2, y+2), text,(0,0,0),font=Font)
        Yazi.text((x-2, y+2), text,(0,0,0),font=Font)
        Yazi.text((x, y), text, (255,255,255), font=Font)
        return

    w, h = Yazi.textsize(Text, Font)
    Satirlar = textwrap.wrap(Text, width=22)
    lastY = -h

    for i in range(0, len(Satirlar)):
        w, h = Yazi.textsize(Satirlar[i], Font)
        x = Foto.width/2 - w/2
        y = i * h
        drawTextWithOutline(Satirlar[i], x, y)

        if Bottom:
            Bottom_Satirlar = textwrap.wrap(BottomText, width=22)
            lastY = Foto.height - h * (len(Bottom_Satirlar) +1) - 10

            for i in range(0, len(Bottom_Satirlar)):
                w, h = Yazi.textsize(Bottom_Satirlar[i], Font)
                x = Foto.width/2 - w/2
                y = lastY + h
                drawTextWithOutline(Bottom_Satirlar[i], x, y)
                lastY = y

    Foto.save("spacememe.png")

@register(outgoing=True, pattern="^.sangmata(?: |$)(.*)")
async def sangmata(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit(LANG['REPLY_MSG'])
       return
    chat = "@SangMataInfo_bot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_BOT_ERROR'])
       return
    await event.edit(LANG['WORKING_ON'])
    async with bot.conversation(chat, exclusive=False) as conv:
          response = None
          try:
              msg = await reply_message.forward_to(chat)
              response = await conv.get_response(message=msg, timeout=5)
          except YouBlockedUserError: 
              await event.edit(LANG['BLOCKED_ERROR'])
              return
          except Exception as e:
              print(e.__class__)

          if not response:
              await event.edit(LANG['NOT_RESPONSE'])
          elif response.text.startswith("Forward"):
             await event.edit(LANG['USER_PRIVACY'])
          else: 
             await event.edit(response.text)
          sleep(1)
          await bot.send_read_acknowledge(chat, max_id=(response.id+3))
          await conv.cancel_all()

@register(outgoing=True, pattern="^.scan")
async def scan(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit(LANG['REPLY_TO_MESSAGE'])
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit(LANG['REPLY_TO_FILE'])
       return
    chat = "@DrWebBot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_USER_ERR'])
       return
    await event.edit(LANG['MIZAH_EXE'])
    async with event.client.conversation(chat) as conv:
      try:     
         response = conv.wait_event(events.NewMessage(incoming=True,from_users=161163358))
         await event.client.forward_messages(chat, reply_message)
         response = await response 
      except YouBlockedUserError:
         await event.reply(LANG['BLOCKED_CHAT'])
         return

      if response.text.startswith("Forward"):
         await event.edit(LANG['USER_PRIVACY'])
      elif response.text.startswith("Select"):
         await event.client.send_message(chat, "English")
         await event.edit(LANG['WAIT_EDIT'])

         response = conv.wait_event(events.NewMessage(incoming=True,from_users=161163358))
         await event.client.forward_messages(chat, reply_message)
         response = conv.wait_event(events.NewMessage(incoming=True,from_users=161163358))
         response = await response
         
         await event.edit(f"**{LANG['SCAN_RESULT']}:**\n {response.message.message}")


      elif response.text.startswith("Still"):
         await event.edit(LANG['SCANNING'])

         response = conv.wait_event(events.NewMessage(incoming=True,from_users=161163358))
         response = await response 
         if response.text.startswith("No threats"):
            await event.edit(LANG['CLEAN'])
         else:
            await event.edit(f"**{LANG['VIRUS_DETECTED']}**\n\nDetaylı bilgi: {response.message.message}")

@register(outgoing=True, pattern="^.creation")
async def creation(event):
    if not event.reply_to_msg_id:
        await event.edit(LANG['REPLY_TO_MSG'])
        return
    reply_message = await event.get_reply_message() 
    if event.fwd_from:
        return 
    chat = "@creationdatebot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    await event.edit(LANG['CALCULATING_TIME'])
    async with event.client.conversation(chat) as conv:
        try:     
            await event.client.forward_messages(chat, reply_message)
        except YouBlockedUserError:
            await event.reply(f"`Pliss buka blokir` {chat} `dulu baru pakai ini.`")
            return
      
        response = conv.wait_event(events.NewMessage(incoming=True,from_users=747653812))
        response = await response
        if response.text.startswith("Looks"):
            await event.edit(LANG['PRIVACY_ERR'])
        else:
            await event.edit(f"**Hasil: **`{response.text.replace('**','')}`")


@register(outgoing=True, pattern="^.ocr2")
async def ocriki(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    chat = "@bacakubot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    await event.edit(LANG['READING'])
    async with event.client.conversation(chat) as conv:
        try:     
            await event.client.forward_messages(chat, reply_message)
        except YouBlockedUserError:
            await event.reply(f"`Pliss buka blokir` {chat} `dulu baru pakai ini.`")
            return
      
        response = conv.wait_event(events.NewMessage(incoming=True,from_users=834289439))
        response = await response
        if response.text.startswith("Pliss coba yang lain..."):
            response = conv.wait_event(events.NewMessage(incoming=True,from_users=834289439))
            response = await response

        if response.text == "":
            await event.edit(LANG['OCR_ERROR'])
        else:
            await event.edit(f"**{LANG['SEE_SOMETHING']}: **`{response.text}`")

@register(outgoing=True, pattern="^.voicy")
async def voicy(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    chat = "@Voicybot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    await event.edit("`Wow ada apakah...`")
    async with event.client.conversation(chat) as conv:
        try:     
            await event.client.forward_messages(chat, reply_message)
        except YouBlockedUserError:
            await event.reply(f"`Pliss buka blokir` {chat} `dulu baru pakai ini.`")
            return
      
        response = conv.wait_event(events.MessageEdited(incoming=True,from_users=259276793))
        response = await response
        if response.text.startswith("__👋"):
            await event.edit(LANG['VOICY_LANG_ERR'])
        elif response.text.startswith("__👮"):
            await event.edit(LANG['VOICY_ERR'])
        else:
            await event.edit(f"**{LANG['HEAR_SOMETHING']}: **`{response.text}`")

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

CmdHelp('scrapers_bot').add_command(
    'sangmata', '<balas ke user>', 'Lihat sejarah nama user.'
).add_command(
    'scan', '<balas ke user>', 'Melihat apakah file yang ditentukan mengandung virus.'
).add_command(
    'meme', '<font> <Up/bottom>', 'Tambahkan teks ke foto. Anda juga dapat menulis ukuran font jika Anda mau.', 'meme 30 iron;ndo'
).add_command(
    'voicy', '<balas ke user>', 'Ubah suara menjadi teks.'
).add_command(
    'q', '<balas ke user>', 'Ubah teks Anda menjadi stiker.'
).add_command(
    'ocr2', '<balas ke user>', 'Baca teks di foto.'
).add_command(
    'creation', '<balas ke user>', 'Cari tahu tanggal pembuatan akun responden Anda.'
).add()
