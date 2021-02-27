from ironbot import BOT_USERNAME
from ironbot.events import register

# ██████ LANGUAGE CONSTANTS ██████ #

from ironbot.language import get_value
LANG = get_value("__helpme")

# ████████████████████████████████ #

@register(outgoing=True, pattern="^.bantuan|^.help")
async def _(event):
    tgbotusername = BOT_USERNAME
    if tgbotusername is not None:
        results = await event.client.inline_query(
            tgbotusername,
            "@ironbot"
        )
        await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
        await event.delete()
    else:
        await event.edit(LANG["NO_BOT"])
