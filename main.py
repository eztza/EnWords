# by Dev EZ

import os
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator

DevEZ = Client(
    "Translator Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TEXT = """
اهلا بك {} في بوت الترجمة ☺
اضغط زر المساعدة لمعرفة كيفية الاستخدام
"""
HELP_TEXT = """
- ارسل فقط الجملة المراد ترجمتها ثم ضع - ثم كود اللغة المراد الترجمة اليها

مثال : `Hello World - ar`

امثلة عن اكواد اللغات والتي تتكون من حرفين فقط :

ar : العربية, en : الانكليزية, fr : الفرنسية

يمكنك الإطلاع على قائمة رموز اللغات [من هنا](https://www.w3.org/WAI/ER/WD-AERT/iso639.htm)
"""
ABOUT_TEXT = """
الاصدار التجريبي من بوت الترجمة الفورية على تيليجرام الخاص بمجموعة بوتات EZ Bots.
قد تواجه بعض الاخطاء عند الترجمة والتي نعمل بشكل دائم على إصلاحها كما نقوم بإضافة العديد من المميزات الفريدة من نوعها والتي ستجدها قريبا في البوت.
"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('كيفية الاستخدام؟', callback_data='help'),
        InlineKeyboardButton('عن البوت', callback_data='about')
        ]]
    )
    
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('الرئيسية', callback_data='home'),
        InlineKeyboardButton('عن البوت', callback_data='about')
        ]]
    )
    
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('قناتنا', url='https://telegram.me/tech_scene')
        ## ,InlineKeyboardButton('اتصل بنا', url='https://telegram.me/')
        ],[
        InlineKeyboardButton('الرئيسية', callback_data='home'),
        InlineKeyboardButton('كيفية الاستخدام', callback_data='help')
        ]]
    )
    
CLOSE_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('إغلاق', callback_data='close')
        ]]
    )
    
TRANSLATE_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('تابعتا', url='https://telegram.me/ezbots_ch'),
        InlineKeyboardButton('حذف النتيجة',callback_data='close')
        ]]
    )
    
DEFAULT_LANGUAGE = os.environ.get("DEFAULT_LANGUAGE", "ar")

@DevEZ.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    else:
        await update.message.delete()
    

@DevEZ.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@DevEZ.on_message((filters.private | filters.group | ~filters.channel) & filters.text)
async def translate(bot, update):
    if update.chat.type == "private":
        if " - " in update.text:
            text, language = update.text.split(" - ", 1)
        else:
            text = update.text
            language = DEFAULT_LANGUAGE
    else:
        text = update.reply_to_message.text
        if " " in update.text:
            command, language = update.text.split(" - ", 1)
        else:
            language = DEFAULT_LANGUAGE
    translator = Translator()
    await update.reply_chat_action("typing")
    message = await update.reply_text("`تتم الترجمة..`")
    try:
        translate = translator.translate(text, dest=language)
        translate_text = f"**تمت الترجمة الى : {language}**"
        translate_text += f"\n\n{translate.text}"
        if len(translate_text) < 4096:
            await message.edit_text(
                text=translate_text,
                disable_web_page_preview=True,
                reply_markup=TRANSLATE_BUTTON
            )
        else:
            with BytesIO(str.encode(str(translate_text))) as translate_file:
                translate_file.name = language + ".txt"
                await update.reply_document(
                    document=translate_file,
                    caption="هذه النسخة التجريبية من البوت، نعمل على اضافة المزيد من التحسينات والخصائص المميزة قريباً",
                    reply_markup=TRANSLATE_BUTTON
                )
                await message.delete()
    except Exception as error:
        print(error)
        await message.edit_text("حدث خطأ، حاول مجدداً..")
        return

DevEZ.run()
