from telethon.tl.types import ChannelParticipantsAdmins
from ironbot import CMD_HELP, bot
from ironbot.events import register
from ironbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.tagall$")
async def _(event):
    if event.fwd_from:
        return
    mentions = "@hallosemua"
    chat = await event.get_input_chat()
    leng = 0
    async for x in bot.iter_participants(chat):
        if leng < 4092:
            mentions += f"[\u2063](tg://user?id={x.id})"
            leng += 1
    await event.reply(mentions)
    await event.delete()

@register(outgoing=True, pattern="^.tagadmin$")
async def _(event):
    if event.fwd_from:
        return
    mentions = "@om"
    chat = await event.get_input_chat()
    async for x in bot.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f"[\u2063](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()

CmdHelp('tagall').add_command(
    'tagall', None, 'Tandai semua orang dalam obrolan saat Anda menggunakan perintah ini.'
).add_command(
    'tagadmin', None, 'Memberi tag pada administrator dalam obrolan saat Anda menggunakan perintah ini.'
).add()