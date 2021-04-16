# Creator @midnightmadwalk to be found on tg and https://github.com/midnightmadwalk on github
# improved by @Lostb053
# further improvement by @Kakashi_HTK/@ashwinstr


from json import dumps

from google_trans_new import google_translator
from googletrans import LANGUAGES

from userge import Message, userge
from userge.plugins.utils.translate import _translate_this

translator = google_translator()


@userge.on_cmd(
    "rom",
    about={
        "header": "Romaji transcriber",
        "supported languages": dumps(LANGUAGES, indent=4, sort_keys=True),
        "flags": {"-s": "transcribe secretly"},
        "usage": "{tr}rom [reply to message or text]",
        "examples": "for other language to latin\n"
        "{tr}rom こんばんは　or　{tr}rom [reply to msg]\n\n"
        "for english to other language translation then script to latin\n"
        "{tr}rom [flag] [[text] or [reply to msg]]",
    },
)
async def romaji_(message: Message):
    x = (
        message.filtered_input_str
        or message.reply_to_message.text
        or message.reply_to_message.caption
    )
    if not x:
        await message.edit("`No input found...`")
        return
    flags = message.flags
    out = ""
    secret = False
    if "-s" in flags:
        secret = True
        if len(flags) > 2:
            await message.edit("Only one language flag supported...", del_in=5)
            return
        elif len(flags) == 2:
            if list(flags)[0] == "-s":
                flag = list(flags)[1]
            else:
                flag = list(flags)[0]
        else:
            no_f = True
    else:
        if len(flags) > 1:
            await message.edit("Only one language flag supported...", del_in=5)
            return
        elif len(flags) == 1:
            flag = list(flags)[0]
    if not secret:
        await message.edit("Transcribing...")
    flag = flag.replace("-", "") if not no_f else False
    if flag:
        try:
            tran = await _translate_this(x, flag, "auto")
            lang_dest = LANGUAGES[f"{tran.dest.lower()}"]
            lang_dest = lang_dest.title()
            lang_src = LANGUAGES[f"{tran.src.lower()}"]
            lang_src = lang_src.title()
            tran = tran.text
        except BaseException:
            await message.edit(
                "Language not supported, check <code>{tr}help rom</code>...", del_in=5
            )
            return
    else:
        try:
            tran = await _translate_this(x, "en", "auto")
            lang_src = LANGUAGES[f"{tran.src.lower()}"]
            lang_src = lang_src.title()
            lang_dest = English
        except BaseException:
            await message.edit("There was some problem...", del_in=5)
            return
        tran = x
    tr_l = translator.detect(tran)
    tr_s = (tran).split("\n")
    try:
        result = translator.translate(
            tr_s, lang_src=tr_l, lang_tgt="en", pronounce=True
        )
    except BaseException:
        await message.edit("Error in transcribing, check <code>{tr}help rom</code>...")
        return
    result = result[1]
    if not secret:
        out += (
            f"Original text from <b>{lang_src}</b>:\n"
            f"<code>{x}</code>\n\n"
            f"Transcribed text to <b>{lang_dest}</b>:\n"
        )
    rom = (
        result.replace("', '", "\n")
        .replace("['", "")
        .replace("']", "")
        .replace("[", "")
        .replace("]", "")
    )
    rom = rom.strip()
    out += f"<code>{rom}</code>"
    await message.edit(out)
