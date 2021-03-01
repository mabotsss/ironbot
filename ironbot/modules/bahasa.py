from ironbot.cmdhelp import CmdHelp
from ironbot import PLUGIN_CHANNEL_ID, CMD_HELP
from ironbot.events import register
from re import search
from json import loads, JSONDecodeError
from ironbot.language import LANGUAGE_JSON
from os import remove

@register(outgoing=True, pattern="^.bahasa ?(.*)")
async def dil(event):
    global LANGUAGE_JSON

    komut = event.pattern_match.group(1)
    if search(r"pasang|install", komut):
        await event.edit("`Memuat file bahasa ... Harap tunggu.`")
        if event.is_reply:
            reply = await event.get_reply_message()
            dosya = await reply.download_media()

            if ((len(reply.file.name.split(".")) >= 2) and (not reply.file.name.split(".")[1] == "ironjson")):
                return await event.edit("`Harap validasi` **IRONJSON** `berikan filenya!`")

            try:
                dosya = loads(open(dosya, "r").read())
            except JSONDecodeError:
                return await event.edit("`Harap validasi` **IRONJSON** `berikan filenya!`")

            await event.edit(f"`{dosya['LANGUAGE']}` `Memuat bahasa...`")
            pchannel = await event.client.get_entity(PLUGIN_CHANNEL_ID)

            dosya = await reply.download_media(file="./ironbot/language/")
            dosya = loads(open(dosya, "r").read())
            await reply.forward_to(pchannel)
            
            LANGUAGE_JSON = dosya
            await event.edit(f"✅ `{dosya['LANGUAGE']}` `bahasa berhasil dipasang!`\n\n**Mulai ulang bot agar transaksi diterapkan!**")
        else:
            await event.edit("**Harap balas ke file bahasa!**")
    elif search(r"hm|info", komut):
        await event.edit("`Mengambil informasi file bahasa ... Harap tunggu.`")
        if event.is_reply:
            reply = await event.get_reply_message()
            if ((len(reply.file.name.split(".")) >= 1) and (not reply.file.name.split(".")[1] == "ironjson")):
                return await event.edit("`Harap validasi` **IRONJSON** `berikan filenya!`")

            dosya = await reply.download_media()

            try:
                dosya = loads(open(dosya, "r").read())
            except JSONDecodeError:
                return await event.edit("`Harap validasi` **IRONJSON** `berikan filenya!`")

            await event.edit(
                f"**Bahasa: **`{dosya['LANGUAGE']}`\n"
                f"**Kode Bahasa: **`{dosya['LANGCODE']}`\n"
                f"**Penerjemah: **`{dosya['AUTHOR']}`\n"

                f"\n\n`Gunakan perintah .bahasa install untuk mengunggah file.`"
            )
        else:
            await event.edit("**Harap balas ke file bahasa!**")
    else:
        await event.edit(
            f"**Bahasa: **`{LANGUAGE_JSON['LANGUAGE']}`\n"
            f"**Kode Bahasa: **`{LANGUAGE_JSON['LANGCODE']}`\n"
            f"**Penerjemah: **`{LANGUAGE_JSON ['AUTHOR']}`\n"

            f"\n\nUntuk bahasa lain, silahkan req ke Developer."
        )

CmdHelp('dil').add_command(
    'bahasa', None, 'Memberikan informasi tentang bahasa yang telah Anda instal.'
).add_command(
    'bahasa info', None, 'Memberikan informasi tentang file bahasa yang Anda tanggapi.'
).add_command(
    'bahasa install', None, 'Mengunggah file bahasa yang Anda tanggapi.'
).add()