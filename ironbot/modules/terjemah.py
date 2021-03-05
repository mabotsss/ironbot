import asyncio
import io
import sys
import time
import traceback
from asyncio.exceptions import TimeoutError

import emoji
from googletrans import Translator
from ironbot.events import register
from ironbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.tr$")
async def _(event):
    input = event.text[4:6]
    txt = event.text[7:]
    xx = await edit_or_replay(event, "`Translating...`")
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input or "en"
    elif input:
        text = txt
        lan = input or "en"
    else:
        return await edit_delete(xx, f"`{hndlr}tr LanguageCode` as reply to a message", time=5)
    text = emoji.demojize(text.strip())
    lan = lan.strip()
    translator = Translator()
    try:
        tt = translator.translate(text, dest=lan)
        output_str = f"**TRANSLATED** from {tt.src} to {lan}\n{tt.text}"
        await edit_delete(xx, output_str)
    except Exception as exc:
        await edit_delete(xx, str(exc), time=10)
        
CmdHelp('terjemah').add_command(
    'tr','<kode negara> <text/balas pesan>', 'translate mbahmu'
).add()
