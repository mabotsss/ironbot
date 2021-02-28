from asyncio import sleep
from re import search, IGNORECASE, escape
from ironbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from ironbot.events import register
from ironbot.cmdhelp import CmdHelp


@register(incoming=True, disable_edited=True, disable_errors=True)
async def filter_incoming_handler(handler):
    try:
        if not (await handler.get_sender()).bot:
            try:
                from ironbot.modules.sql_helper.filter_sql import get_filters
            except AttributeError:
                await handler.edit("`Running on Non-SQL mode!`")
                return
            name = handler.raw_text
            filters = get_filters(handler.chat_id)
            if not filters:
                return
            for trigger in filters:
                pattern = (
                    r"( |^|[^\w])" + escape(trigger.keyword) + r"( |$|[^\w])")
                pro = search(pattern, name, flags=IGNORECASE)
                if pro and trigger.f_mesg_id:
                    msg_o = await handler.client.get_messages(
                        entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id))
                    await handler.reply(msg_o.message, file=msg_o.media)
                elif pro and trigger.reply:
                    await handler.reply(trigger.reply)
    except AttributeError:
        pass


@register(outgoing=True, pattern=r"^.filter (.*)")
async def add_new_filter(new_handler):
    try:
        from ironbot.modules.sql_helper.filter_sql import add_filter
    except AttributeError:
        await new_handler.edit("`Running on Non-SQL mode!`")
        return
    value = new_handler.pattern_match.group(1).split(None, 1)
    keyword = value[0]
    try:
        string = value[1]
    except IndexError:
        string = None
    msg = await new_handler.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await new_handler.client.send_message(
                BOTLOG_CHATID, f"#FILTER\nCHAT ID: {new_handler.chat_id}\nKATA: {keyword}"
                "\n\nPesan berikut disimpan sebagai data balasan filter untuk obrolan, jangan dihapus !!"
            )
            msg_o = await new_handler.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=new_handler.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            return await new_handler.edit(
                "`Menyimpan media sebagai balasan ke filter memerlukan penyetelan BOTLOG_CHATID.`"
            )
    elif new_handler.reply_to_msg_id and not string:
        rep_msg = await new_handler.get_reply_message()
        string = rep_msg.text
    success = "`Filter`  **{}**  `{} berhasil di update`."
    if add_filter(str(new_handler.chat_id), keyword, string, msg_id) is True:
        await new_handler.edit(success.format(keyword, 'added'))
    else:
        await new_handler.edit(success.format(keyword, 'updated'))
        await asyncio.sleep(2)
        await new_handler.delete()


@register(outgoing=True, pattern=r"^.stop (.*)")
async def remove_a_filter(r_handler):
    try:
        from ironbot.modules.sql_helper.filter_sql import remove_filter
    except AttributeError:
        return await r_handler.edit("`Running on Non-SQL mode!`")
    filt = r_handler.pattern_match.group(1)
    if not remove_filter(r_handler.chat_id, filt):
        await r_handler.edit("`Filter`  **{}**  `tidak ada`.".format(filt))
    else:
        await r_handler.edit(
            "`Filter`  **{}**  `berhasil dihapus`.".format(filt))


@register(outgoing=True, pattern="^.rmfilters (.*)")
async def kick_marie_filter(event):
    bot_type = event.pattern_match.group(1).lower()
    if bot_type not in ["marie", "rose"]:
        return await event.edit("`Bot itu belum didukung!`")
    await event.edit("```Akan menendang semua Filters!```")
    await sleep(3)
    resp = await event.get_reply_message()
    filters = resp.text.split("-")[1:]
    for i in filters:
        if bot_type.lower() == "marie":
            await event.reply("/stop %s" % (i.strip()))
        if bot_type.lower() == "rose":
            i = i.replace('`', '')
            await event.reply("/stop %s" % (i.strip()))
        await sleep(0.3)
    await event.respond(
        "```Berhasil membersihkan filter bot yaay!```!")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "aku menghapus semua filter di " + str(event.chat_id))


@register(outgoing=True, pattern="^.filters$")
async def filters_active(event):
    try:
        from ironbot.modules.sql_helper.filter_sql import get_filters
    except AttributeError:
        return await event.edit("`Running on Non-SQL mode!`")
    transact = "`Tidak ada filter dalam obrolan ini.`"
    filters = get_filters(event.chat_id)
    for filt in filters:
        if transact == "`Tidak ada filter dalam obrolan ini.`":
            transact = "Filter aktif dalam obrolan ini :\n"
            transact += "🔺 `{}`\n".format(filt.keyword)
        else:
            transact += "🔺 `{}`\n".format(filt.keyword)

    await event.edit(transact)


CmdHelp('filters').add_command(
    'filters', None, 'Menampilkan semua filter ironbot dalam obrolan.'
).add_command(
    'filter', '<kata> <balasan respon> atau pesan .filter <kata>', 'Menambahkan filter setiap kali kata yang Anda tambahkan ditulis, bot akan merespons.', 'filter "contoh" "respon contoh"'
).add_command(
    'stop', '<filter>', 'Menghentikan filter yang dipilih.'
).add_command(
    'rmfilters', None, 'menghapus semua filter'
).add()