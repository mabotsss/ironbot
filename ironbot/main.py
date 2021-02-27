import importlib
from importlib import import_module
from sqlite3 import connect
import os
import platform
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetMessagesRequest
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP, LANGUAGE, IRON_VERSION, PATTERNS
from .modules import ALL_MODULES
import ironbot.modules.sql_helper.mesaj_sql as MSJ_SQL
import ironbot.modules.sql_helper.galeri_sql as GALERI_SQL
from pySmartDL import SmartDL
from telethon.tl import functions
from telethon import __version__ as tv
from random import choice
import chromedriver_autoinstaller
from json import loads, JSONDecodeError
import re
import ironbot.cmdhelp

DIZCILIK_STR = [
     "Saya sedang mengedit stiker ...",
     "Hidup memesan ...",
     "Saya mengundang stiker ini ke paket saya ...",
     "Saya harus memperbaiki ini ...",
     "Hei, ini stiker yang bagus!",
     "Aku meratakan stikermu \nhahaha.",
     "Hei lihat di sana. (☉｡☉)! → \n Selagi aku mengedit ini ...",
     "Mawar merah violet biru, aku akan keren dengan menempelkan stiker ini di ranselku ...",
     "Stiker dipenjara ...",
     "Tuan cantik mengerjai stiker ini ...",
]

AFKSTR = [
    "Aku sedang terburu-buru sekarang, tidak bisakah kau mengirimiku pesan nanti? Aku akan kembali juga.",
    "Orang yang Anda panggil tidak dapat menjawab telepon sekarang. Anda dapat meninggalkan pesan Anda dengan tarif Anda sendiri setelah nada. Biaya pesan 49 kurus. \ N`biiiiiiiiiiiiiiiiiiiiiiiiiiip`!",
    "Aku akan kembali dalam beberapa menit. Tapi jika tidak ... tunggu lebih lama.",
    "Saya tidak di sini sekarang, saya mungkin di tempat lain.",
    "Mawar itu merah \nMawar berwarna biru \nTinggalkan aku pesan \nDan aku akan menghubungi kamu kembali.",
    "Terkadang hal terbaik dalam hidup layak untuk ditunggu… \nAku akan segera kembali.",
    "Saya akan segera kembali, tetapi jika saya tidak kembali, saya akan kembali lagi nanti.",
    "Jika Anda belum mengerti, saya tidak di sini.",
    "Halo, selamat datang di pesan jauh saya, bagaimana saya bisa mengabaikan Anda hari ini?",
    "Saya jauh dari 7 lautan dan 7 negara, \n7 perairan dan 7 benua, \n7 gunung dan 7 bukit, \n7 dataran dan 7 gundukan, \n7 kolam dan 7 danau, \n7 mata air dan 7 padang rumput, \n7 kota dan 7 lingkungan, \n7 blok dan 7 rumah ... \n \nTempat di mana bahkan pesan tidak bisa sampai ke saya! ",
    "Saya sedang jauh dari keyboard sekarang, tetapi jika Anda berteriak cukup keras di layar Anda, saya dapat mendengar Anda.",
    "Saya bergerak ke arah berikut \n ---->",
    "Saya bergerak ke arah berikut \n <----",
    "Silakan tinggalkan pesan dan buat saya merasa lebih penting daripada sebelumnya.",
    "Pemilik saya tidak ada di sini, jadi berhentilah menulis kepada saya.",
    "Jika aku ada di sini, \nAku akan memberitahumu di mana aku berada. \ N \nTapi bukan aku, \ ketika aku kembali tanyakan padaku ...",
    "Aku pergi! \nAku tidak tahu kapan aku akan kembali! \ NSaya berharap beberapa menit!",
    "Pemilik saya tidak tersedia sekarang. Jika Anda memberikan nama, nomor dan alamat Anda, saya dapat mengirimkannya kepadanya dan begitu dia kembali.",
    "Maaf, pemilik saya tidak ada di sini. Anda dapat berbicara dengan saya sampai dia datang. \ Ndia akan kembali kepada Anda nanti.",
    "Saya yakin Anda mengharapkan pesan!",
    "Hidup ini terlalu singkat, ada banyak hal yang harus dilakukan ... \nAku melakukan salah satunya ...",
    "Aku tidak di sini sekarang .... \n tapi jika aku ... \n \n bukankah itu bagus?",
]

UNAPPROVED_MSG = ("`Hey,` {mention}`! .\n\n`"
                  "`Pemilik saya tidak memberi Anda izin kepada PM. `"
                  "`Harap tunggu pemilik saya aktif, dia biasanya mengkonfirmasi PM.\n\n`"
                  "`Sejauh yang saya tahu dia tidak mengizinkan orang untuk PM.`")

DB = connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nLAPORAN: Nomor telepon yang dimasukkan tidak valid' \
             '\n  Tip: Masukkan nomor Anda menggunakan kode negara Anda' \
             '\n       Periksa kembali nomor telepon Anda'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("learning-data-root.check").close()

def extractCommands(file):
    FileRead = open(file, 'r').read()
    
    if '/' in file:
        file = file.split('/')[-1]

    Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", FileRead)
    Komutlar = []

    if re.search(r'CmdHelp\(.*\)', FileRead):
        pass
    else:
        dosyaAdi = file.replace('.py', '')
        CmdHelp = ironbot.cmdhelp.CmdHelp(dosyaAdi, False)

        # Komutları Alıyoruz #
        for Command in Pattern:
            Command = Command[1]
            if Command == '' or len(Command) <= 1:
                continue
            Komut = re.findall("(^.*[a-zA-Z0-9şğüöçı]\w)", Command)
            if (len(Komut) >= 1) and (not Komut[0] == ''):
                Komut = Komut[0]
                if Komut[0] == '^':
                    KomutStr = Komut[1:]
                    if KomutStr[0] == '.':
                        KomutStr = KomutStr[1:]
                    Komutlar.append(KomutStr)
                else:
                    if Command[0] == '^':
                        KomutStr = Command[1:]
                        if KomutStr[0] == '.':
                            KomutStr = KomutStr[1:]
                        else:
                            KomutStr = Command
                        Komutlar.append(KomutStr)

            Ironpy = re.search('\"\"\"IRONPY(.*)\"\"\"', FileRead, re.DOTALL)
            if not Ironpy == None:
                Ironpy = Ironpy.group(0)
                for Satir in Ironpy.splitlines():
                    if (not '"""' in Satir) and (':' in Satir):
                        Satir = Satir.split(':')
                        Isim = Satir[0]
                        Deger = Satir[1][1:]
                                
                        if Isim == 'INFO':
                            CmdHelp.add_info(Deger)
                        elif Isim == 'WARN':
                            CmdHelp.add_warning(Deger)
                        else:
                            CmdHelp.set_file_info(Isim, Deger)
            for Komut in Komutlar:
                # if re.search('\[(\w*)\]', Komut):
                    # Komut = re.sub('(?<=\[.)[A-Za-z0-9_]*\]', '', Komut).replace('[', '')
                CmdHelp.add_command(Komut, None, 'Plugin ini telah dipasang secara eksternal. Tidak ada deskripsi yang ditentukan.')
            CmdHelp.add()

try:
    bot.start()
    idim = bot.get_me().id
    ironbl = requests.get('https://gitlab.com/Quiec/asen/-/raw/master/asen.json').json()
    if idim in ironbl:
        bot.disconnect()

    # ChromeDriver'ı Ayarlayalım #
    try:
        chromedriver_autoinstaller.install()
    except:
        pass
    
    # Galeri için değerler
    GALERI = {}

    # PLUGIN MESAJLARI AYARLIYORUZ
    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": "`🐺 Ironbots Aktif.`", "afk": f"`{str(choice(AFKSTR))}`", "kickme": "`byebyee `🤠", "pm": UNAPPROVED_MSG, "dızcı": str(choice(DIZCILIK_STR)), "ban": "{mention}`, terlarang!`", "mute": "{mention}`, meredam!`", "approve": "{mention}`, Anda dapat mengirimi saya pesan!`", "disapprove": "{mention}`, Anda tidak diizinkan untuk mengirim pesan!`", "block": "{mention}`, Anda diblokir!`"}

    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "kickme", "pm", "dızcı", "ban", "mute", "approve", "disapprove", "block"]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDYA_"):
                medya = int(dmsj.split("MEDYA_")[1])
                medya = bot.get_messages(PLUGIN_CHANNEL_ID, ids=medya)

                PLUGIN_MESAJLAR[mesaj] = medya
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
    if not PLUGIN_CHANNEL_ID == None:
        LOGS.info("Loading plugin")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
        except:
            KanalId = "me"

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if plugin.file.name and (len(plugin.file.name.split('.')) > 1) \
                and plugin.file.name.split('.')[-1] == 'py':
                Split = plugin.file.name.split('.')

                if not os.path.exists("./ironbot/modules/" + plugin.file.name):
                    dosya = bot.download_media(plugin, "./ironbot/modules/")
                else:
                    LOGS.info("Plugin Ini Sudah Dipasang " + plugin.file.name)
                    extractCommands('./ironbot/modules/' + plugin.file.name)
                    dosya = plugin.file.name
                    continue 
                
                try:
                    spec = importlib.util.spec_from_file_location("ironbot.modules." + Split[0], dosya)
                    mod = importlib.util.module_from_spec(spec)

                    spec.loader.exec_module(mod)
                except Exception as e:
                    LOGS.info(f"`Gagal mengunggah! Plugin salah.\n\nERROR: {e}`")

                    try:
                        plugin.delete()
                    except:
                        pass

                    if os.path.exists("./ironbot/modules/" + plugin.file.name):
                        os.remove("./ironbot/modules/" + plugin.file.name)
                    continue
                extractCommands('./ironbot/modules/' + plugin.file.name)
    else:
        bot.send_message("me", f"`Harap setel PLUGIN_CHANNEL_ID untuk plugin menjadi permanen.`")
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

async def FotoDegistir (foto):
    FOTOURL = GALERI_SQL.TUM_GALERI[foto].foto
    r = requests.get(FOTOURL)

    with open(str(foto) + ".jpg", 'wb') as f:
        f.write(r.content)    
    file = await bot.upload_file(str(foto) + ".jpg")
    try:
        await bot(functions.photos.UploadProfilePhotoRequest(
            file
        ))
        return True
    except:
        return False

for module_name in ALL_MODULES:
    imported_module = import_module("ironbot.modules." + module_name)


LOGS.info(f"""
-------------------------------------------
🇮🇩 Ironbot-reborn Based On Telethon V{tv}
🐍 Python Version : {platform.python_version()}
🛡 Ironbot-reborn Version : {IRON_VERSION}
💙 Dev : @ndourbae
🛑 Thanks to : @freedom_reborn
-------------------------------------------""")


"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()