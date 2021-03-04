from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.types import User
from sqlalchemy.exc import IntegrityError

from ironbot import (COUNT_PM, CMD_HELP, BOTLOG, BOTLOG_CHATID,
                     PM_AUTO_BAN, PM_AUTO_BAN_LIMIT, LASTMSG, LOGS, BRAIN_CHECKER, WHITELIST, ALIVE_NAME)
from ironbot.events import register
from ironbot.main import PLUGIN_MESAJLAR
from ironbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from ironbot.language import get_value
LANG = get_value("pmpermit")

# ████████████████████████████████ #

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node

DEF_UNAPPROVED_MSG = (
    f"__**ROOM CHAT || {DEFAULTUSER}**__\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    f"```HALLO SELAMAT DATANG, SAYA ADALAH BOT YANG MENJAGA ROOM CHAT INI MOHON JANGAN MELAKUKAN SPAM KARNA SAYA OTOMATIS AKAN MEMBLOKIR ANDA, TUNGGU SAMPAI {DEFAULTUSER} MENERIMA PESAN ANDA```\n"
    "┏━━━━━━━━━━━━━━━━━━━\n"
    "┣[• `PESAN OTOMATIS`\n"
    "┣[• `BY IRONBOT`\n"
    "┗━━━━━━━━━━━━━━━━━━━")

@register(incoming=True, disable_edited=True, disable_errors=True)
async def permitpm(event):
    if PM_AUTO_BAN:
        self_user = await event.client.get_me()
        if event.is_private and event.chat_id != 777000 and event.chat_id != self_user.id and not (
                await event.get_sender()).bot:
            try:
                from ironbot.modules.sql_helper.pm_permit_sql import is_approved
                from ironbot.modules.sql_helper.globals import gvarstatus
            except AttributeError:
                return
            apprv = is_approved(event.chat_id)
            notifsoff = gvarstatus("NOTIF_OFF")
            
            getmsg = gvarstatus("unapproved_msg")
            if getmsg is not None:
                UNAPPROVED_MSG = getmsg
            else:
                UNAPPROVED_MSG = PLUGIN_MESAJLAR['pm']

            reply_user = await event.get_sender()
            id = reply_user.id
            first_name = str(reply_user.first_name)
            if reply_user.last_name:
                last_name = str(reply_user.last_name)
            else:
                last_name = ''

            username = '@' + reply_user.username if reply_user.username else f'[{first_name} {last_name}](tg://user?id={id})'
            mention = f'[{first_name} {last_name}](tg://user?id={id})'

            if not apprv and event.text != UNAPPROVED_MSG:
                if event.chat_id in LASTMSG:
                    prevmsg = LASTMSG[event.chat_id]
                    if event.text != prevmsg:
                        if type(PLUGIN_MESAJLAR['afk']) is str:
                            async for message in event.client.iter_messages(
                                event.chat_id,
                                from_user='me',
                                search=UNAPPROVED_MSG.format(
                                    id=id,
                                    username=username,
                                    mention=first_name,
                                    first_name=first_name,
                                    last_name=last_name
                                )
                            ):
                                await message.delete()
                            await event.reply(UNAPPROVED_MSG.format(
                                id=id,
                                username=username,
                                mention=mention,
                                first_name=first_name,
                                last_name=last_name
                            ))
                        else:
                            async for message in event.client.iter_messages(
                                event.chat_id,
                                from_user='me',
                                limit=PM_AUTO_BAN_LIMIT + 1):
                                    await message.delete()
                            if not UNAPPROVED_MSG.text == '':
                                UNAPPROVED_MSG.text = UNAPPROVED_MSG.text.format(
                                    id=id,
                                    username=username,
                                    mention=mention,
                                    first_name=first_name,
                                    last_name=last_name
                                )

                            await event.reply(UNAPPROVED_MSG)
                    LASTMSG.update({event.chat_id: event.text})
                else:
                    await event.reply(UNAPPROVED_MSG.format(
                                    id=id,
                                    username=username,
                                    mention=mention,
                                    first_name=first_name,
                                    last_name=last_name
                                ))
                    LASTMSG.update({event.chat_id: event.text})

                if notifsoff:
                    await event.client.send_read_acknowledge(event.chat_id)
                if event.chat_id not in COUNT_PM:
                    COUNT_PM.update({event.chat_id: 1})
                else:
                    COUNT_PM[event.chat_id] = COUNT_PM[event.chat_id] + 1

                if COUNT_PM[event.chat_id] > PM_AUTO_BAN_LIMIT:
                    await event.respond(
                        LANG['BLOCKED']
                    )

                    try:
                        del COUNT_PM[event.chat_id]
                        del LASTMSG[event.chat_id]
                    except KeyError:
                        if BOTLOG:
                            await event.client.send_message(
                                BOTLOG_CHATID,
                                LANG['ERROR'],
                            )
                        LOGS.info(
                            LANG['ERROR'])
                        return

                    await event.client(BlockRequest(event.chat_id))
                    await event.client(ReportSpamRequest(peer=event.chat_id))

                    if BOTLOG:
                        name = await event.client.get_entity(event.chat_id)
                        name0 = str(name.first_name)
                        await event.client.send_message(
                            BOTLOG_CHATID,
                            "[" + name0 + "](tg://user?id=" +
                            str(event.chat_id) + ")" +
                            LANG['BOTLOG_BLOCKED'],
                        )


@register(disable_edited=True, outgoing=True, disable_errors=True)
async def auto_accept(event):
    if not PM_AUTO_BAN:
        return
    self_user = await event.client.get_me()
    if event.is_private and event.chat_id != 777000 and event.chat_id != self_user.id and not (
            await event.get_sender()).bot:
        try:
            from ironbot.modules.sql_helper.pm_permit_sql import is_approved
            from ironbot.modules.sql_helper.pm_permit_sql import approve
        except AttributeError:
            return

        getmsg = gvarstatus("unapproved_msg")
        if getmsg is not None:
            UNAPPROVED_MSG = getmsg
        else:
            UNAPPROVED_MSG = PLUGIN_MESAJLAR['pm']

        chat = await event.get_chat()
        id = chat.id
        first_name = str(chat.first_name)
        if chat.last_name:
            last_name = str(chat.last_name)
        else:
            last_name = ''

        username = '@' + chat.username if chat.username else f'[{first_name} {last_name}](tg://user?id={id})'
        mention = f'[{first_name} {last_name}](tg://user?id={id})'

        if isinstance(chat, User):
            if is_approved(event.chat_id) or chat.bot:
                return
            async for message in event.client.iter_messages(event.chat_id,
                                                            reverse=True,
                                                            limit=1):
                if type(PLUGIN_MESAJLAR['afk']) is str:
                    if message.message is not UNAPPROVED_MSG.format(
                                    id=id,
                                    username=username,
                                    mention=mention,
                                    first_name=first_name,
                                    last_name=last_name
                                ) and message.from_id == self_user.id:
                        try:
                            approve(event.chat_id)
                        except IntegrityError:
                            return
                else:
                    if message is not UNAPPROVED_MSG and message.from_id == self_user.id:
                        try:
                            approve(event.chat_id)
                        except IntegrityError:
                            return


                if is_approved(event.chat_id) and BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "#DISETUJUI OTOMATIS\n" + "Username: " +
                        f"[{chat.first_name}](tg://user?id={chat.id})",
                    )


@register(outgoing=True, pattern="^.notifoff$")
async def notifoff(noff_event):
    try:
        from ironbot.modules.sql_helper.globals import addgvar
    except AttributeError:
        await noff_event.edit("`Bot Non-SQL bekerja!!`")
        return
    addgvar("NOTIF_OFF", True)
    await noff_event.edit(LANG['NOTIFOFF'])


@register(outgoing=True, pattern="^.notifon$")
async def notifon(non_event):
    try:
        from ironbot.modules.sql_helper.globals import delgvar
    except:
        await non_event.edit("`Bot Non-SQL bekerja!!`")
        return
    delgvar("NOTIF_OFF")
    await non_event.edit(LANG['NOTIFON'])


@register(outgoing=True, pattern="^.approve$|^.ap$")
async def approvepm(apprvpm):
    try:
        from ironbot.modules.sql_helper.pm_permit_sql import approve
    except:
        await apprvpm.edit("`Bot Non-SQL bekerja!!`")
        return

    if apprvpm.reply_to_msg_id:
        reply = await apprvpm.get_reply_message()
        reply_user = await apprvpm.client.get_entity(reply.from_id)
    else:
        reply_user = await apprvpm.client.get_entity(apprvpm.chat_id)

    getmsg = gvarstatus("unapproved_msg")
    if getmsg is not None:
         UNAPPROVED_MSG = getmsg
    else:
         UNAPPROVED_MSG = PLUGIN_MESAJLAR['pm']


    id = reply_user.id
    first_name = str(reply_user.first_name)
    if reply_user.last_name:
        last_name = str(reply_user.last_name)
    else:
        last_name = ''

    username = '@' + reply_user.username if reply_user.username else f'[{first_name} {last_name}](tg://user?id={id})'
    mention = f'[{first_name} {last_name}](tg://user?id={id})'

    try:
        approve(id)
    except IntegrityError:
        await apprvpm.edit(LANG['ALREADY'])
        return

    await apprvpm.edit(PLUGIN_MESAJLAR['approve'].format(
        id=id,
        username=username,
        mention=mention,
        first_name=first_name,
        last_name=last_name
    ))
    async for message in apprvpm.client.iter_messages(apprvpm.chat_id,
                                                      from_user='me',
                                                      search=UNAPPROVED_MSG.format(
        id=id,
        username=username,
        mention=first_name,
        first_name=first_name,
        last_name=last_name
    )):
    	await apprvpm.delete(getmsg)
        await message.delete()

    if BOTLOG:
        await apprvpm.client.send_message(
            BOTLOG_CHATID,
            "#DISETUJUI\n" + "Username: " + mention,
        )


@register(outgoing=True, pattern="^.disapprove$|^.dp$")
async def disapprovepm(disapprvpm):
    try:
        from ironbot.modules.sql_helper.pm_permit_sql import dissprove
    except:
        await disapprvpm.edit("`Bot Non-SQL bekerja!!`")
        return

    if disapprvpm.reply_to_msg_id:
        reply = await disapprvpm.get_reply_message()
        replied_user = await disapprvpm.client.get_entity(reply.from_id)
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        dissprove(replied_user.id)
    else:
        dissprove(disapprvpm.chat_id)
        aname = await disapprvpm.client.get_entity(disapprvpm.chat_id)
        name0 = str(aname.first_name)

    await disapprvpm.edit(PLUGIN_MESAJLAR['disapprove'].format(mention = f"[{name0}](tg://user?id={disapprvpm.chat_id})"))

    if BOTLOG:
        await disapprvpm.client.send_message(
            BOTLOG_CHATID,
            f"[{name0}](tg://user?id={disapprvpm.chat_id})"
            " Tidak diizinkan untuk PM",
        )


@register(outgoing=True, pattern="^.block$")
async def blockpm(block):
    if block.reply_to_msg_id:
        reply = await block.get_reply_message()
        replied_user = await block.client.get_entity(reply.from_id)
        if replied_user.id in BRAIN_CHECKER or replied_user.id in WHITELIST:
            await block.edit(
                "`Aku gabisa memblokir penciptaku!!`"
            )
            return

        id = replied_user.id
        first_name = str(replied_user.first_name)
        if replied_user.last_name:
            last_name = str(replied_user.last_name)
        else:
            last_name = ''

        username = '@' + replied_user.username if replied_user.username else f'[{first_name} {last_name}](tg://user?id={id})'
        mention = f'[{first_name} {last_name}](tg://user?id={id})'
        await block.client(BlockRequest(replied_user.id))
        await block.edit(PLUGIN_MESAJLAR['block'].format(
            id=id,
            username=username,
            mention=mention,
            first_name=first_name,
            last_name=last_name
        ))
    else:
        if block.chat_id in BRAIN_CHECKER:
            await block.edit(
                "`Aku gabisa memblokir penciptaku!!`"
            )
            return

        await block.client(BlockRequest(block.chat_id))
        replied_user = await block.client.get_entity(block.chat_id)
        id = replied_user.id
        first_name = str(replied_user.first_name)
        if replied_user.last_name:
            last_name = str(replied_user.last_name)
        else:
            last_name = ''

        username = '@' + replied_user.username if replied_user.username else f'[{first_name} {last_name}](tg://user?id={id})'
        mention = f'[{first_name} {last_name}](tg://user?id={id})'

        await block.edit(PLUGIN_MESAJLAR['block'].format(
            id=id,
            username=username,
            mention=mention,
            first_name=first_name,
            last_name=last_name
        ))
    try:
        from ironbot.modules.sql_helper.pm_permit_sql import dissprove
        dissprove(id)
    except:
        pass

    if BOTLOG:
        await block.client.send_message(
            BOTLOG_CHATID,
            "#DIBLOKIR\n" + "Username: " + mention,
        )


@register(outgoing=True, pattern="^.unblock$")
async def unblockpm(unblock):
    if unblock.reply_to_msg_id:
        reply = await unblock.get_reply_message()
        replied_user = await unblock.client.get_entity(reply.from_id)
        name0 = str(replied_user.first_name)
        await unblock.client(UnblockRequest(replied_user.id))
        await unblock.edit(f"`{LANG['UNBLOCKED']}`")

    if BOTLOG:
        await unblock.client.send_message(
            BOTLOG_CHATID,
            f"[{name0}](tg://user?id={replied_user.id})"
            "tidak diblokir.",
        )
        
        
@register(outgoing=True, pattern=r"^.(set|get|reset) pm_msg(?: |$)(\w*)")
async def add_pmsg(cust_msg):
    """Set your own Unapproved message"""
    if not PM_AUTO_BAN:
        return await cust_msg.edit("** Anda Harus Menyetel** `PM_AUTO_BAN` **Ke** `True`")
    try:
        import ironbot.modules.sql_helper.globals as sql
    except AttributeError:
        await cust_msg.edit("`Running on Non-SQL mode!`")
        return

    await cust_msg.edit("`Sedang Memproses...`")
    conf = cust_msg.pattern_match.group(1)

    custom_message = sql.gvarstatus("unapproved_msg")

    if conf.lower() == "set":
        message = await cust_msg.get_reply_message()
        status = "Pesan"

        # check and clear user unapproved message first
        if custom_message is not None:
            sql.delgvar("unapproved_msg")
            status = "Pesan"

        if message:
            # TODO: allow user to have a custom text formatting
            # eg: bold, underline, striketrough, link
            # for now all text are in monoscape
            msg = message.message  # get the plain text
            sql.addgvar("unapproved_msg", msg)
        else:
            return await cust_msg.edit("`Mohon Balas Ke Pesan`")

        await cust_msg.edit("`Pesan Berhasil Disimpan Ke Room Chat`")

        if BOTLOG:
            await cust_msg.client.send_message(
                BOTLOG_CHATID, f"**{status} PM Yang Tersimpan Dalam Room Chat Anda:** \n\n{msg}"
            )

    if conf.lower() == "reset":
        if custom_message is not None:
            sql.delgvar("unapproved_msg")
            await cust_msg.edit("`Anda Telah Menghapus Pesan Custom PM Ke Default`")
        else:
            await cust_msg.edit("`Pesan PM Anda Sudah Default Sejak Awal`")

    if conf.lower() == "get":
        if custom_message is not None:
            await cust_msg.edit(
                "**Ini Adalah Pesan PM Yang Sekarang Dikirimkan Ke Room Chat Anda:**" f"\n\n{custom_message}"
            )
        else:
            await cust_msg.edit(
                "*Anda Belum Menyetel Pesan PM*\n"
                f"Masih Menggunakan Pesan PM Default: \n\n`{DEF_UNAPPROVED_MSG}`"
            )
                                       

CmdHelp('pmpermit').add_command(
    'approve', None, 'Memberi izin untuk PM.', 
).add_command(
    'disapprove', None, 'Tidak diizinkan untuk PM.'
).add_command(
    'block', '<username / reply> ',' Blokir pengguna. '
).add_command(
    'unblock', '<username / reply> ',' Batalkan pemblokiran pengguna.'
).add_command(
    'notifoff', None, 'Menghapus atau menonaktifkan pemberitahuan pesan pribadi yang tidak disetujui.'
).add_command(
    'notifon', None, 'Izinkan pesan pribadi yang tidak disetujui untuk mengirim pemberitahuan.'
).add()