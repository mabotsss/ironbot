from . import LANGUAGE, LOGS, bot, PLUGIN_CHANNEL_ID
from json import loads, JSONDecodeError
from os import path, remove
from telethon.tl.types import InputMessagesFilterDocument

pchannel = bot.get_entity(PLUGIN_CHANNEL_ID)
LOGS.info("Pemuatan file bahasa...")
LANGUAGE_JSON = None

for dil in bot.iter_messages(pchannel, filter=InputMessagesFilterDocument):
    if ((len(dil.file.name.split(".")) >= 2) and (dil.file.name.split(".")[1] == "ironjson")):
        if path.isfile(f"./ironbot/language/{dil.file.name}"):
            try:
                LANGUAGE_JSON = loads(open(f"./ironbot/language/{dil.file.name}", "r").read())
            except JSONDecodeError:
                dil.delete()
                remove(f"./ironbot/language/{dil.file.name}")

                if path.isfile("./ironbot/language/DEFAULT.ironjson"):
                    LOGS.warn("File bahasa default digunakan...")
                    LANGUAGE_JSON = loads(open(f"./ironbot/language/DEFAULT.ironjson", "r").read())
                else:
                    raise Exception("Bahasa salah")
        else:
            try:
                DOSYA = dil.download_media(file="./ironbot/language/")
                LANGUAGE_JSON = loads(open(DOSYA, "r").read())
            except JSONDecodeError:
                dil.delete()
                if path.isfile("./ironbot/language/DEFAULT.ironjson"):
                    LOGS.warn("File bahasa default digunakan...")
                    LANGUAGE_JSON = loads(open(f"./ironbot/language/DEFAULT.ironjson", "r").read())
                else:
                    raise Exception("Bahasa salah")
        break

if LANGUAGE_JSON == None:
    if path.isfile(f"./ironbot/language/{LANGUAGE}.ironjson"):
        try:
            LANGUAGE_JSON = loads(open(f"./ironbot/language/{LANGUAGE}.ironjson", "r").read())
        except JSONDecodeError:
            raise Exception("json file tidak cocok")
    else:
        if path.isfile("./ironbot/language/DEFAULT.ironjson"):
            LOGS.warn("File bahasa default digunakan...")
            LANGUAGE_JSON = loads(open(f"./ironbot/language/DEFAULT.ironjson", "r").read())
        else:
            raise Exception(f"Tidak dapat menemukan {LANGUAGE} file")

LOGS.info(f"Bahasa {LANGUAGE_JSON['LANGUAGE']} dimuat.")

def get_value (plugin = None, value = None):
    global LANGUAGE_JSON

    if LANGUAGE_JSON == None:
        raise Exception("Pliss load bahasa terlebih dahulu")
    else:
        if not plugin == None or value == None:
            Plugin = LANGUAGE_JSON.get("STRINGS").get(plugin)
            if Plugin == None:
                raise Exception("plugin gagal")
            else:
                String = LANGUAGE_JSON.get("STRINGS").get(plugin).get(value)
                if String == None:
                    return Plugin
                else:
                    return String
        else:
            raise Exception("plugin / string salah")