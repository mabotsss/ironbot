from ironbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from ironbot.events import register
from asyncio import sleep
from ironbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from ironbot.language import get_value
LANG = get_value("notes")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.notes$")
async def notes_active(svd):
    try:
        from ironbot.modules.sql_helper.notes_sql import get_notes
    except AttributeError:
        await svd.edit("`Bot Non-SQL!!`")
        return
    message = LANG['NOT_FOUND']
    notes = get_notes(svd.chat_id)
    for note in notes:
        if message == LANG['NOT_FOUND']:
            message = f"{LANG['NOTES']}:\n"
            message += "`#{}`\n".format(note.keyword)
        else:
            message += "`#{}`\n".format(note.keyword)
    await svd.edit(message)


@register(outgoing=True, pattern=r"^.clear (\w*)")
async def remove_notes(clr):
    try:
        from ironbot.modules.sql_helper.notes_sql import rm_note
    except AttributeError:
        await clr.edit("`Bot Non-SQL!!`")
        return
    notename = clr.pattern_match.group(1)
    if rm_note(clr.chat_id, notename) is False:
        return await clr.edit(" **{}** `{}`".format(notename, LANG['CLEAR_NOT_FOUND']))
    else:
        return await clr.edit(
            "**{}** `{}`".format(notename, LANG['CLEAR']))


@register(outgoing=True, pattern=r"^.save (\w*)")
async def add_note(fltr):
    try:
        from ironbot.modules.sql_helper.notes_sql import add_note
    except AttributeError:
        await fltr.edit("`Bot Non-SQL!!`")
        return
    keyword = fltr.pattern_match.group(1)
    string = fltr.text.partition(keyword)[2]
    msg = await fltr.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await fltr.client.send_message(
                BOTLOG_CHATID, f"#NOTE\
            \nGrup ID: {fltr.chat_id}\
            \nAnahtar kelime: {keyword}\
            \n\nBu mesaj sohbette notu cevaplamak için kaydedildi, lütfen bu mesajı silmeyin!"
            )
            msg_o = await fltr.client.forward_messages(entity=BOTLOG_CHATID,
                                                       messages=msg,
                                                       from_peer=fltr.chat_id,
                                                       silent=True)
            msg_id = msg_o.id
        else:
            await fltr.edit(
                "`Untuk menyimpan media sebagai catatan, nilai BOTLOG_CHATID harus disetel.`"
            )
            return
    elif fltr.reply_to_msg_id and not string:
        rep_msg = await fltr.get_reply_message()
        string = rep_msg.text
    success = "`{} {}. ` #{} `{}`"
    if add_note(str(fltr.chat_id), keyword, string, msg_id) is False:
        return await fltr.edit(success.format(LANG['SUCCESS'], 'diperbarui', keyword, LANG['CALL']))
    else:
        return await fltr.edit(success.format(LANG['SUCCESS'], 'ditambahkan', keyword, LANG['CALL']))


@register(pattern=r"#\w*",
          disable_edited=True,
          disable_errors=True,
          ignore_unsafe=True)
async def incom_note(getnt):
    try:
        if not (await getnt.get_sender()).bot:
            try:
                from ironbot.modules.sql_helper.notes_sql import get_note
            except AttributeError:
                return
            notename = getnt.text[1:]
            note = get_note(getnt.chat_id, notename)
            message_id_to_reply = getnt.message.reply_to_msg_id
            if not message_id_to_reply:
                message_id_to_reply = None
            if note and note.f_mesg_id:
                msg_o = await getnt.client.get_messages(entity=BOTLOG_CHATID,
                                                        ids=int(
                                                            note.f_mesg_id))
                await getnt.client.send_message(getnt.chat_id,
                                                msg_o.mesage,
                                                reply_to=message_id_to_reply,
                                                file=msg_o.media)
            elif note and note.reply:
                await getnt.client.send_message(getnt.chat_id,
                                                note.reply,
                                                reply_to=message_id_to_reply)
    except AttributeError:
        pass

CmdHelp('notes').add_command(
    '#<notes>', None, 'Melihat isi catatan yang dipilih.'
).add_command(
    'save', '<nama notes> <isi notes> atau pesan .save <nama notes> balas ke pesan. ', 'Menyimpan pesan yang dibalas dengan namanya sebagai catatan. (Juga berfungsi pada gambar, dokumen, dan stiker.)'
).add_command(
    'notes', None, 'Menampilkan semua catatan dalam chat.'
).add_command(
    'clear', '<nama notes>', 'Menghapus notes yang dipilih.'
).add()