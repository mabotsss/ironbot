import os
import time
from datetime import datetime
from re import compile
from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from dotenv import load_dotenv
from requests import get
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sync import TelegramClient, custom
from telethon.sessions import StringSession
from telethon.events import callbackquery, InlineQuery, NewMessage
from math import ceil
from telethon import Button, events

load_dotenv("config.env")

# Bot 
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

ASYNC_POOL = []

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - @Ironbots - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - @Ironbots - %(levelname)s - %(message)s",
                level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 6:
    LOGS.info("Anda harus memiliki setidaknya versi python 3.6 atau lebih tinggi"
              "Beberapa fitur bergantung padanya. Bot sedang dimatikan.")
    quit(1)

CONFIG_CHECK = os.environ.get(
    "___________LUTFEN_______BU_____SATIRI_____SILIN__________", None)

if CONFIG_CHECK:
    LOGS.info(
        "Harap hapus baris yang ditentukan dalam hashtag pertama dari file config.env"
    )
    quit(1)

LANGUAGE = os.environ.get("LANGUAGE", "DEFAULT").upper()

if not LANGUAGE in ["EN", "TR", "AZ", "UZ", "DEFAULT"]:
    LOGS.info("Anda mengetik dalam bahasa yang tidak dikenal. Oleh karena itu, DEFAULT digunakan.")
    LANGUAGE = "DEFAULT"
    
    
IRON_VERSION = "v3.0.7"

API_KEY = os.environ.get("API_KEY", None)
API_HASH = os.environ.get("API_HASH", None)

SILINEN_PLUGIN = {}

STRING_SESSION = os.environ.get("STRING_SESSION", None)

BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", None))

# UserBot
BOTLOG = sb(os.environ.get("BOTLOG", "False"))
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "False"))

PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

HEROKU_MEMEZ = sb(os.environ.get("HEROKU_MEMEZ", "False"))
HEROKU_APPNAME = os.environ.get("HEROKU_APPNAME", None)
HEROKU_APIKEY = os.environ.get("HEROKU_APIKEY", None)

UPSTREAM_REPO_URL = os.environ.get(
    "UPSTREAM_REPO_URL",
    "https://github.com/mabotsss/ironbot.git")

CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

DB_URI = os.environ.get("DATABASE_URL", "sqlite:///iron.db")

OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)

REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)

# AUTO PP
AUTO_PP = os.environ.get("AUTO_PP", None)

# Warn 
WARN_LIMIT = int(os.environ.get("WARN_LIMIT", 3))
WARN_MODE = os.environ.get("WARN_MODE", "gmute")

if not WARN_MODE in ["gmute", "gban"]:
    WARN_MODE = "gmute"

# Galeri
GALERI_SURE = int(os.environ.get("GALERI_SURE", 60))

CHROME_DRIVER = os.environ.get("CHROME_DRIVER", None)
GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN", None)

PLUGINID = os.environ.get("PLUGIN_CHANNEL_ID", None)
# Plugin 
if not PLUGINID:
    PLUGIN_CHANNEL_ID = "me"
else:
    PLUGIN_CHANNEL_ID = int(PLUGINID)

# OpenWeatherMap API Key
OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
WEATHER_DEFCITY = os.environ.get("WEATHER_DEFCITY", None)

# Lydia API
LYDIA_API_KEY = os.environ.get("LYDIA_API_KEY", None)

# Anti Spambot
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

# Youtube API key
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)

COUNTRY = str(os.environ.get("COUNTRY", ""))
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

BIO_PREFIX = os.environ.get("BIO_PREFIX", "@Ironbots | ")
DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)

LASTFM_API = os.environ.get("LASTFM_API", None)
LASTFM_SECRET = os.environ.get("LASTFM_SECRET", None)
LASTFM_USERNAME = os.environ.get("LASTFM_USERNAME", None)
LASTFM_PASSWORD_PLAIN = os.environ.get("LASTFM_PASSWORD", None)
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)
if LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
    lastfm = LastFMNetwork(api_key=LASTFM_API,
                           api_secret=LASTFM_SECRET,
                           username=LASTFM_USERNAME,
                           password_hash=LASTFM_PASS)
else:
    lastfm = None

# Google Drive 
G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA", None)
GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", None)
TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY",
                                         "./downloads")

# Inline bot
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)

GENIUS = os.environ.get("GENIUS", None)
CMD_HELP = {}
CMD_HELP_BOT = {}
PM_AUTO_BAN_LIMIT = int(os.environ.get("PM_AUTO_BAN_LIMIT", 4))

SPOTIFY_DC = os.environ.get("SPOTIFY_DC", None)
SPOTIFY_KEY = os.environ.get("SPOTIFY_KEY", None)

NAMA_PACK = os.environ.get("NAMA_PACK", "@Ironbots")

OTOMATIS_JOIN = sb(os.environ.get("OTOMATIS_JOIN", "True"))

PATTERNS = os.environ.get("PATTERNS", ".;!,")
WHITELIST = get('https://raw.githubusercontent.com/mabotsss/ironbot/master/resources/whitelist.json').json()

if not os.path.exists('bin'):
    os.mkdir('bin')

binaries = {
    "https://raw.githubusercontent.com/yshalsager/megadown/master/megadown":
    "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py":
    "bin/cmrudl"
}

for binary, path in binaries.items():
    downloader = SmartDL(binary, path, progress_bar=False)
    downloader.start()
    os.chmod(path, 0o755)

# 'bot'
if STRING_SESSION:
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    bot = TelegramClient("ironbot", API_KEY, API_HASH)


if os.path.exists("learning-data-root.check"):
    os.remove("learning-data-root.check")
else:
    LOGS.info("Loading...")

URL = 'https://raw.githubusercontent.com/mabotsss/ironbot/master/resources/rooted/learning-data-root.check'
with open('learning-data-root.check', 'wb') as load:
    load.write(get(URL).content)

async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "Anda perlu menyetel variabel BOTLOG_CHATID dari konfigurasi agar log kesalahan khusus berfungsi.")
        quit(1)

    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "Agar fitur logging berfungsi, Anda harus menyetel variabel BOTLOG_CHATID dari konfigurasi.")
        quit(1)

    elif not BOTLOG or not LOGSPAMMER:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Akun Anda tidak diizinkan untuk mengirim pesan ke grup BOTLOG_CHATID. "
            "Periksa apakah Anda mengetik ID grup dengan benar.")
        quit(1)
        
if not BOT_TOKEN == None:
    tgbot = TelegramClient(
        "TG_BOT_TOKEN",
        api_id=API_KEY,
        api_hash=API_HASH
    ).start(bot_token=BOT_TOKEN)
else:
    tgbot = None

def butonlastir(sayfa, moduller):
    Satir = 4
    Kolon = 2
    
    moduller = sorted([modul for modul in moduller if not modul.startswith("_")])
    pairs = list(map(list, zip(moduller[::2], moduller[1::2])))
    if len(moduller) % 2 == 1:
        pairs.append([moduller[-1]])
    max_pages = ceil(len(pairs) / Satir)
    pairs = [pairs[i:i + Satir] for i in range(0, len(pairs), Satir)]
    butonlar = []
    for pairs in pairs[sayfa]:
        butonlar.append([
            custom.Button.inline("🔸 " + pair, data=f"bilgi[{sayfa}]({pair})") for pair in pairs
        ])

    butonlar.append([custom.Button.inline("◀️ ᴋᴇᴍʙᴀʟɪ", data=f"sayfa({(max_pages - 1) if sayfa == 0 else (sayfa - 1)})"), custom.Button.inline("-ᴄʟᴏꜱᴇ-", data="closes"), custom.Button.inline("ʟᴀɴᴊᴜᴛ ▶️", data=f"sayfa({0 if sayfa == (max_pages - 1) else sayfa + 1})")])
    return [max_pages, butonlar]

with bot:
    if OTOMATIS_JOIN:
        try:
            bot(JoinChannelRequest("@Ironbots"))
            bot(JoinChannelRequest("@freedom_reborn"))
        except:
            pass

    moduller = CMD_HELP
    me = bot.get_me()
    uid = me.id

    try:
        @tgbot.on(NewMessage(pattern='/start'))
        async def start_bot_handler(event):
            if not event.message.from_id == uid:
                await event.reply(f'`Hai aku` @ironbot`! Maboss (`@{me.username}`) ')
            else:
                await event.reply(f'`Ironbot berjalan normal... 🤖`')

        @tgbot.on(InlineQuery)  # pylint:disable=E0602
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query == "@ironbot":
                rev_text = query[::-1]
                veriler = (butonlastir(0, sorted(CMD_HELP)))
                result = await builder.article(
                    f"Harap Gunakan Hanya Dengan Perintah .help",
                    text=f"**🤖 ʜᴀʟʟᴏᴏ ɪɴɪ ᴀᴅᴀʟᴀʜ !** [ɪʀᴏɴʙᴏᴛꜱ](https://t.me/ironbots)\n\n`Total plugin: {len(CMD_HELP)} | ʜᴀʟᴀᴍᴀɴ: 1/{veriler[0]}`",
                    buttons=veriler[1],
                    link_preview=False
                )
            elif query.startswith("http"):
                parca = query.split(" ")
                result = builder.article(
                    "File Diunggah",
                    text=f"**File berhasil {parca[2]} diunggah ke situs!**\n\nWaktu pemuatan: {parca[1][:3]} kedua\n[‏‏‎ ‎]({parca[0]})",
                    buttons=[
                        [custom.Button.url('URL', parca[0])]
                    ],
                    link_preview=True
                )
            else:
                result = builder.article(
                    "@ironbots",
                    text="""@ironbots coba gunakan!
Anda dapat mengubah akun Anda menjadi bot dan menggunakannya. Ingat, Anda tidak dapat mengelola bot orang lain! Semua detail penyiapan dijelaskan dari GitHub di bawah ini.""",
                    buttons=[
                        [custom.Button.url("Bergabunglah dengan Channel", "https://t.me/freedom_reborn"), custom.Button.url(
                            "Grub", "https://t.me/freedom_reborn")],
                        [custom.Button.url(
                            "GitHub", "https://github.com/xscrprog/ironbot")]
                    ],
                    link_preview=False
                )
            await event.answer([result] if result else None)

        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"sayfa\((.+?)\)")))
        async def sayfa(event):
            if not event.query.user_id == uid: 
                return await event.answer("Pasang ironbot sendiri gan, biar ga kepo wkwkwk 🤣.", cache_time=0, alert=True)
            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            veriler = butonlastir(sayfa, CMD_HELP)
            await event.edit(
                f"**🤖 ʜᴀʟʟᴏᴏ ɪɴɪ ᴀᴅᴀʟᴀʜ !** [ɪʀᴏɴʙᴏᴛꜱ](https://t.me/freedom_reborn)\n\n`Total plugin: {len(CMD_HELP)} | ʜᴀʟᴀᴍᴀɴ: {sayfa + 1}/{veriler[0]}`",
                buttons=veriler[1],
                link_preview=False
            )
            
            
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"closes")))
        async def closes(event):
            if event.query.user_id == uid:
               buttons = [
               [
                   Button.inline("📗ᴍᴇɴᴜ", data="opensss"),
                   custom.Button.url("❤ᴅᴇᴠ", "https://t.me/ndourbae"),
               ],
                   [Button.inline("•ᴘɪɴɢ•", data="pingsss")],
                   [Button.inline("•ᴛʜᴀɴᴋꜱ ᴛᴏ•", data="thnksto")],
                   [Button.inline("••ᴇxɪᴛ••", data="exitsss")],
               ]
               await event.edit(
                   f"`ᴍᴇɴᴜ ᴅɪ ᴛᴜᴛᴜᴘ\nᴛᴏᴛᴀʟ ᴘʟᴜɢɪɴ : {len(CMD_HELP)}`",
                   buttons=buttons,
                   link_preview=False,
                )
            else:
                reply_pop_up_alert = "❌  Pasang ironbot sendiri gan, biar ga kepo wkwkwk 🤣."
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"pingsss")))
        async def _(event):
            start = datetime.now()
            end = datetime.now()
            ms = (end - start).microseconds / 100
            pin = f"🌋Pɪɴɢ = {ms}ms"
            await event.answer(pin, cache_time=0, alert=True)
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"thnksto")))
        async def _(event):
            await event.answer("Akun Telegram : \n\n👤 @incorrect_cuy\n👤 @Mantulity\n👤 @Bryan066\n👤 @planktoneye\n👤 @XINKQ_Chan", cache_time=0, alert=True)
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"exitsss")))
        async def opensss(event):
            if not event.query.user_id == uid:
                return await event.answer("❌ Pasang ironbot sendiri gan, biar ga kepo wkwkwk 🤣.", cache_time=0, alert=True)
            await event.edit("**BERHASIL KELUAR**")
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"opensss")))
        async def opensss(event):
            if not event.query.user_id == uid:
                return await event.answer("❌ Pasang ironbot sendiri gan, biar ga kepo wkwkwk 🤣.", cache_time=0, alert=True)
            veriler = (butonlastir(0, sorted(CMD_HELP)))
            await event.edit(
                f"**🤖 ʜᴀʟʟᴏᴏ ɪɴɪ ᴀᴅᴀʟᴀʜ !** [ɪʀᴏɴʙᴏᴛꜱ](https://t.me/freedom_reborn)\n\n`Total plugin: {len(CMD_HELP)} | ʜᴀʟᴀᴍᴀɴ: 1/{veriler[0]}`",
                buttons=veriler[1],
                link_preview=False
            )           
            
            
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"bilgi\[(\d*)\]\((.*)\)")))
        async def bilgi(event):
            if not event.query.user_id == uid: 
                return await event.answer("Pasang ironbot sendiri gan, biar ga kepo wkwkwk 🤣.", cache_time=0, alert=True)

            sayfa = int(event.data_match.group(1).decode("UTF-8"))
            komut = event.data_match.group(2).decode("UTF-8")
            try:
                butonlar = [custom.Button.inline("🔹 " + cmd[0], data=f"komut[{komut}[{sayfa}]]({cmd[0]})") for cmd in CMD_HELP_BOT[komut]['commands'].items()]
            except KeyError:
                return await event.answer("❌ Tidak ada deskripsi tertulis untuk modul ini.", cache_time=0, alert=True)

            butonlar = [butonlar[i:i + 2] for i in range(0, len(butonlar), 2)]
            butonlar.append([custom.Button.inline("◀️ ᴋᴇᴍʙᴀʟɪ", data=f"sayfa({sayfa})")])
            await event.edit(
                f"**📗 Tips untuk:** `{komut}`\n**🔢 Jumlah Perintah:** `{len(CMD_HELP_BOT[komut]['commands'])}`",
                buttons=butonlar,
                link_preview=False
            )
        
        @tgbot.on(callbackquery.CallbackQuery(data=compile(b"komut\[(.*)\[(\d*)\]\]\((.*)\)")))
        async def komut(event):
            if not event.query.user_id == uid: 
                return await event.answer("Pasang ironbot sendiri gan, biar ga kepo wkwkwk 🤣.", cache_time=0, alert=True)

            cmd = event.data_match.group(1).decode("UTF-8")
            sayfa = int(event.data_match.group(2).decode("UTF-8"))
            komut = event.data_match.group(3).decode("UTF-8")

            result = f"**📗 Tips untuk:** `{cmd}`\n"
            if CMD_HELP_BOT[cmd]['info']['info'] == '':
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⬇️ Official:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                    result += f"**⚠️ Peringatan:** {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
                else:
                    result += f"**⬇️ Official:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n\n"
            else:
                result += f"**⬇️ Official:** {'✅' if CMD_HELP_BOT[cmd]['info']['official'] else '❌'}\n"
                if not CMD_HELP_BOT[cmd]['info']['warning'] == '':
                    result += f"**⚠️ Peringatan:** {CMD_HELP_BOT[cmd]['info']['warning']}\n"
                result += f"**ℹ️ Info:** {CMD_HELP_BOT[cmd]['info']['info']}\n\n"

            command = CMD_HELP_BOT[cmd]['commands'][komut]
            if command['params'] is None:
                result += f"**🛠 Perintah:** `{PATTERNS[:1]}{command['command']}`\n"
            else:
                result += f"**🛠 Perintah:** `{PATTERNS[:1]}{command['command']} {command['params']}`\n"
                
            if command['example'] is None:
                result += f"**💬 Penjelasan:** `{command['usage']}`\n\n"
            else:
                result += f"**💬 Penjelasan:** `{command['usage']}`\n"
                result += f"**⌨️ Contoh:** `{PATTERNS[:1]}{command['example']}`\n\n"

            await event.edit(
                result,
                buttons=[custom.Button.inline("◀️ ᴋᴇᴍʙᴀʟɪ", data=f"bilgi[{sayfa}]({cmd})")],
                link_preview=False
            )
    except Exception as e:
        print(e)
        LOGS.info(
            "Dukungan sebaris dinonaktifkan di bot Anda."
            "Untuk mengaktifkan, tentukan token bot dan aktifkan mode sebaris pada bot Anda."
            "Jika menurut Anda ada masalah selain ini, hubungi kami."
        )

    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except:
        LOGS.info(
            "Variabel lingkungan BOTLOG_CHATID bukan entitas yang valid. "
            "Periksa variabel lingkungan / file config.env Anda."
        )
        quit(1)


SON_GORULME = 0
COUNT_MSG = 0
USERS = {}
BRAIN_CHECKER = []
COUNT_PM = {}
LASTMSG = {}
ENABLE_KILLME = True
ISAFK = False
AFKREASON = None
ZALG_LIST = [[
    "̖",
    " ̗",
    " ̘",
    " ̙",
    " ̜",
    " ̝",
    " ̞",
    " ̟",
    " ̠",
    " ̤",
    " ̥",
    " ̦",
    " ̩",
    " ̪",
    " ̫",
    " ̬",
    " ̭",
    " ̮",
    " ̯",
    " ̰",
    " ̱",
    " ̲",
    " ̳",
    " ̹",
    " ̺",
    " ̻",
    " ̼",
    " ͅ",
    " ͇",
    " ͈",
    " ͉",
    " ͍",
    " ͎",
    " ͓",
    " ͔",
    " ͕",
    " ͖",
    " ͙",
    " ͚",
    " ",
],
    [
    " ̍", " ̎", " ̄", " ̅", " ̿", " ̑", " ̆", " ̐", " ͒", " ͗",
    " ͑", " ̇", " ̈", " ̊", " ͂", " ̓", " ̈́", " ͊", " ͋", " ͌",
    " ̃", " ̂", " ̌", " ͐", " ́", " ̋", " ̏", " ̽", " ̉", " ͣ",
    " ͤ", " ͥ", " ͦ", " ͧ", " ͨ", " ͩ", " ͪ", " ͫ", " ͬ", " ͭ",
    " ͮ", " ͯ", " ̾", " ͛", " ͆", " ̚"
],
    [
    " ̕",
    " ̛",
    " ̀",
    " ́",
    " ͘",
    " ̡",
    " ̢",
    " ̧",
    " ̨",
    " ̴",
    " ̵",
    " ̶",
    " ͜",
    " ͝",
    " ͞",
    " ͟",
    " ͠",
    " ͢",
    " ̸",
    " ̷",
    " ͡",
]]
