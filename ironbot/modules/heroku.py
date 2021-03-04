import codecs
import heroku3
import aiohttp
import math
import os
import requests
import asyncio

from ironbot import (
    HEROKU_APPNAME,
    HEROKU_APIKEY,
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    bot)
    
from ironbot.events import register
from ironbot.cmdhelp import CmdHelp

heroku_api = "https://api.heroku.com"
if HEROKU_APPNAME is not None and HEROKU_APIKEY is not None:
    Heroku = heroku3.from_key(HEROKU_APIKEY)
    app = Heroku.app(HEROKU_APPNAME)
    heroku_var = app.config()
else:
    app = None



@register(outgoing=True,
          pattern=r"^.(get|del) var(?: |$)(\w*)")
async def variable(var):
    exe = var.pattern_match.group(1)
    if app is None:
        await var.edit("`[HEROKU]"
                       "\nHarap Siapkan`  **HEROKU_APPNAME**.")
        return False
    if exe == "get":
        await var.edit("`Mendapatkan Informasi...`")
        variable = var.pattern_match.group(2)
        if variable != '':
            if variable in heroku_var:
                if BOTLOG:
                    await var.client.send_message(
                        BOTLOG_CHATID, "#ConfigVars\n\n"
                        "**Config Vars**:\n"
                        f"`{variable}` **=** `{heroku_var[variable]}`\n"
                    )
                    await var.edit("`Diterima Ke BOTLOG_CHATID...`")
                    return True
                else:
                    await var.edit("`Mohon Ubah BOTLOG Ke True...`")
                    return False
            else:
                await var.edit("`Informasi Tidak Ditemukan...`")
                return True
        else:
            configvars = heroku_var.to_dict()
            msg = ''
            if BOTLOG:
                for item in configvars:
                    msg += f"`{item}` = `{configvars[item]}`\n"
                await var.client.send_message(
                    BOTLOG_CHATID, "#CONFIGVARS\n\n"
                    "**Config Vars**:\n"
                    f"{msg}"
                )
                await var.edit("`Diterima Ke BOTLOG_CHATID`")
                return True
            else:
                await var.edit("`Mohon Ubah BOTLOG Ke True`")
                return False
    elif exe == "del":
        await var.edit("`Menghapus Config Vars... ヅ`")
        variable = var.pattern_match.group(2)
        if variable == '':
            await var.edit("`Mohon Tentukan Config Vars Yang Mau Anda Hapus`")
            return False
        if variable in heroku_var:
            if BOTLOG:
                await var.client.send_message(
                    BOTLOG_CHATID, "#MenghapusConfigVars\n\n"
                    "**Menghapus Config Vars**:\n"
                    f"`{variable}`"
                )
            await var.edit("`Config Vars Telah Dihapus`")
            del heroku_var[variable]
        else:
            await var.edit("`Tidak Dapat Menemukan Config Vars`")
            return True


@register(outgoing=True, pattern=r'^.set var (\w*) ([\s\S]*)')
async def set_var(var):
    await var.edit("`Sedang Menyetel Config Vars ヅ`")
    variable = var.pattern_match.group(1)
    value = var.pattern_match.group(2)
    if variable in heroku_var:
        if BOTLOG:
            await var.client.send_message(
                BOTLOG_CHATID, "#SetelConfigVars\n\n"
                "**Mengganti Config Vars**:\n"
                f"`{variable}` = `{value}`"
            )
        await var.edit("`Sedang Proses, Mohon Menunggu Dalam Beberapa Detik ヅ`")
    else:
        if BOTLOG:
            await var.client.send_message(
                BOTLOG_CHATID, "#MenambahkanConfigVar\n\n"
                "**Menambahkan Config Vars**:\n"
                f"`{variable}` **=** `{value}`"
            )
        await var.edit("`Menambahkan Config Vars....`")
    heroku_var[variable] = value


@register(outgoing=True, pattern=r"^.usage(?: |$)")
async def dyno_usage(dyno):
    await dyno.edit("`Mendapatkan Informasi Dyno Heroku Anda ヅ...`")
    useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/80.0.3987.149 Mobile Safari/537.36'
                 )
    u_id = Heroku.account().id
    headers = {
     'User-Agent': useragent,
     'Authorization': f'Bearer {HEROKU_APIKEY}',
     'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + u_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("`Tidak Bisa Mendapatkan Informasi Dyno ヅ`\n\n"
                               f">.`{r.reason}`\n")
    result = r.json()
    quota = result['account_quota']
    quota_used = result['quota_used']

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result['apps']
    try:
        App[0]['quota_used']
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]['quota_used'] / 60
        AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)
    
    return await dyno.edit(
                f"**☛ Informasi Dyno**: {app.name}\n\n╭━┯━━━━━━━━━━━━━━━━┯━╮\n"
                f"✥ `Penggunaan Dyno` **{app.name}**:\n"
                f"  ❉ **{AppHours} Jam - "
                f"{AppMinutes} Menit  -  {AppPercentage}%**"
                "\n ✲━─━─━─━─━─━─━─━─━─━✲\n"
                "✥ `Sisa Dyno Bulan Ini`:\n"
                f"  ❉ **{hours} Jam - {minutes} Menit  "
                f"-  {percentage}%**\n"
                "╰━┷━━━━━━━━━━━━━━━━┷━╯"
            )


@register(outgoing=True, pattern=r"^\.logs")
async def _(dyno):
    try:
        Heroku = heroku3.from_key(HEROKU_APIKEY)
        app = Heroku.app(HEROKU_APPNAME)
    except BaseException:
        return await dyno.reply(
            "`Please make sure your Heroku API Key, Your App name are configured correctly in the heroku var.`"
        )
    await dyno.edit("`Sedang Mengambil Logs  ヅ`")
    with open("logs.txt", "w") as log:
        log.write(app.get_log())
    fd = codecs.open("logs.txt", "r", encoding="utf-8")
    data = fd.read()
    key = (requests.post("https://nekobin.com/api/documents",
                         json={"content": data}) .json() .get("result") .get("key"))
    url = f"https://nekobin.com/raw/{key}"
    await dyno.edit(f"`Ini Logs Heroku Anda :`\n\nPaste Ke: [Nekobin]({url})")
    return os.remove("logs.txt")

@register(outgoing=True, pattern=r"^\.xlogs")
async def giblog(event):
    if event.fwd_from:
        return
    Heroku = heroku3.from_key(HEROKU_APIKEY)
    app = Heroku.app(HEROKU_APPNAME)
  #  herokuHelper = HerokuHelper(HEROKU_APPNAME, HEROKU_APIKEY)
  #  logz = herokuHelper.getLog()
    with open("logs.txt", "w") as log:
        log.write(app.get_log())
    await event.delete()
    await bot.send_file(
        event.chat_id, "logs.txt", caption=f"**Logs Of {Config.HEROKU_APP_NAME}**"
    )

CmdHelp('heroku').add_command(
'usage', None, 'Memberikan informasi tentang jam dyno..'
    ).add_command(
        'set var', None, 'set var <Nama Var baru> <Nilai> ConfigVar baru ditambahkan ke bot Anda.'
    ).add_command(
        'get var', None, 'Dapatkan VAR Anda saat ini, hanya tersedia di grup botlog Anda .'
    ).add_command(
        'del var', None, 'del var <Nama var> Setelah menghapus ConfigVar yang telah Anda pilih, masukkan .restart ke bot Anda.'
    ).add_command(
        'logs', None, 'Heroku logs'
    ).add()