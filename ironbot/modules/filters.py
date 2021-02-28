import asyncio
import re

from telethon import utils
from telethon.tl import types
from ironbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from ironbot.events import register
from ironbot.cmdhelp import CmdHelp

from ironbot.modules.sql_helper.filter_sql import (
    add_filter,
    get_all_filters,
    remove_all_filters,
    remove_filter,
)

DELETE_TIMEOUT = 0
TYPE_TEXT = 0
TYPE_PHOTO = 1
TYPE_DOCUMENT = 2


global last_triggered_filters
last_triggered_filters = {}  # pylint:disable=E0602


@register(incoming=True, disable_edited=True, disable_errors=True)
async def on_snip(event):
    global last_triggered_filters
    name = event.raw_text
    if event.chat_id in last_triggered_filters:
        if name in last_triggered_filters[event.chat_id]:
            # avoid ironbot spam
            # "I demand rights for us bots, we are equal to you humans." -Henri Koivuneva (t.me/UserbotTesting/2698)
            return False
    snips = get_all_filters(event.chat_id)
    if snips:
        for snip in snips:
            pattern = r"( |^|[^\w])" + re.escape(snip.keyword) + r"( |$|[^\w])"
            if re.search(pattern, name, flags=re.IGNORECASE):
                if snip.snip_type == TYPE_PHOTO:
                    media = types.InputPhoto(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference,
                    )
                elif snip.snip_type == TYPE_DOCUMENT:
                    media = types.InputDocument(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference,
                    )
                else:
                    media = None
                event.message.id
                if event.reply_to_msg_id:
                    event.reply_to_msg_id
                await event.reply(snip.reply, file=media)
                if event.chat_id not in last_triggered_filters:
                    last_triggered_filters[event.chat_id] = []
                last_triggered_filters[event.chat_id].append(name)
                await asyncio.sleep(DELETE_TIMEOUT)
                last_triggered_filters[event.chat_id].remove(name)


@register(outgoing=True, pattern="^.filter (.*)")
async def on_snip_save(event):
    if event.fwd_from:
        return
    hitler = await edit_or_reply(event, "Processing....")
    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if msg:
        snip = {"type": TYPE_TEXT, "text": msg.message or ""}
        if msg.media:
            media = None
            if isinstance(msg.media, types.MessageMediaPhoto):
                media = utils.get_input_photo(msg.media.photo)
                snip["type"] = TYPE_PHOTO
            elif isinstance(msg.media, types.MessageMediaDocument):
                media = utils.get_input_document(msg.media.document)
                snip["type"] = TYPE_DOCUMENT
            if media:
                snip["id"] = media.id
                snip["hash"] = media.access_hash
                snip["fr"] = media.file_reference
        add_filter(
            event.chat_id,
            name,
            snip["text"],
            snip["type"],
            snip.get("id"),
            snip.get("hash"),
            snip.get("fr"),
        )
        await hitler.edit(f"filter {name} saved successfully. Get it with {name}")
    else:
        await hitler.edit(
            "Reply to a message with `savefilter keyword` to save the filter"
        )


@register(outgoing=True, pattern="^.filters (.*)")
async def on_snip_list(event):
    if event.fwd_from:
        return
    indiaislove = await edit_or_reply(event, "Processing....")
    all_snips = get_all_filters(event.chat_id)
    OUT_STR = "Available Filters in the Current Chat:\n"
    if len(all_snips) > 0:
        for a_snip in all_snips:
            OUT_STR += f"{a_snip.keyword} \n"
    else:
        OUT_STR = "No Filters. Start Saving using `.filter`"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "filters.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available Filters in the Current Chat",
                reply_to=event,
            )
            await event.delete()
    else:
        await indiaislove.edit(OUT_STR)


@register(outgoing=True, pattern="^.stop (.*)")
async def on_snip_delete(event):
    if event.fwd_from:
        return
    iloveindia = await edit_or_reply(event, "Processing...")
    name = event.pattern_match.group(1)
    remove_filter(event.chat_id, name)
    await iloveindia.edit(f"filter {name} deleted successfully")


@register(outgoing=True, pattern="^.rmfilters$")
async def on_all_snip_delete(event):
    if event.fwd_from:
        return
    edit_or_reply(event, "Processing....")
    remove_all_filters(event.chat_id)
    await event.edit(f"filters **in current chat** deleted successfully")


CmdHelp('filter').add_command(
    'filters', None, 'Menampilkan semua filter ironbot dalam obrolan.'
).add_command(
    'filter', '<kata> <balasan respon> atau pesan .filter <kata>', 'Menambahkan filter setiap kali kata yang Anda tambahkan ditulis, bot akan merespons.', 'filter "contoh" "respon contoh"'
).add_command(
    'stop', '<filter>', 'Menghentikan filter yang dipilih.'
).add_command(
    'rmfilters', None, 'menghapus semua filter'
).add()