# (c) @AbirHasan2005 | @PredatorHackerzZ

import asyncio
from urllib.parse import quote_plus
from configs import Config
from pyrogram import Client
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.errors import FloodWait
from handlers.helpers import str_to_b64
from hashids import Hashids
from handlers.database import db

hashids = Hashids(salt="This is a very very secured string")

def encode_string(string):
    encoded = hashids.encode(*[ord(c) for c in string])
    return encoded

async def forward_to_own_channel(bot: Client, message: Message, editable: Message, DB_OWN_CHANNEL):
    try:
        __SENT = await message.forward(DB_OWN_CHANNEL)
        return __SENT
    except FloodWait as sl:
        if sl.value > 45:
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text=f"#FloodWait:\nGot FloodWait of `{str(sl.value)}s` from `{str(editable.chat.id)}` !!",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Owner", url ="https://telegram.me/rushidhar1999")]
                    ]
                )
            )
        return await forward_to_own_channel(bot, message, editable, DB_OWN_CHANNEL)

async def forward_to_channel(bot: Client, message: Message, editable: Message):
    try:
        __SENT = await message.forward(Config.DB_CHANNEL)
        return __SENT
    except FloodWait as sl:
        if sl.value > 45:
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text=f"#FloodWait:\nGot FloodWait of `{str(sl.value)}s` from `{str(editable.chat.id)}` !!",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Owner", url ="https://telegram.me/rushidhar1999")]
                    ]
                )
            )
        return await forward_to_channel(bot, message, editable)


async def save_batch_media_in_channel(bot: Client, editable: Message, message_ids: list):
    own = False
    try:
        DB_OWN_CHANNEL = await db.exist_channel_id(editable.reply_to_message.from_user.id)
        if DB_OWN_CHANNEL:
            try:
                bot_status = await bot.get_chat_member(DB_OWN_CHANNEL, int(Config.BOT_ID))
                user = await bot.get_chat_member(DB_OWN_CHANNEL, editable.reply_to_message.from_user.id)
                if (bot_status.privileges.can_post_messages and str(user.status) in ["ChatMemberStatus.ADMINISTRATOR", "ChatMemberStatus.CREATOR", "ChatMemberStatus.OWNER"]):
                    own = True
                else:
                    await bot.send_message(
                        chat_id=int(editable.chat.id),
                        text=f"<b>⚠️ You Should Be Admin In Channel_ID, Make Bot Admin And Give Post Messages Permission For Bot In Channel_ID, The Link Now Generated Was Not From Your Channel_ID ⚠️</b>",
                        disable_web_page_preview=True,
                    )
            except:
                await bot.send_message(
                    chat_id=int(editable.chat.id),
                    text=f"<b>⚠️ You Should Be Admin In Channel_ID, Make Bot Admin And Give Post Messages Permission For Bot In Channel_ID, The Link Now Generated Was Not From Your Channel_ID ⚠️</b>",
                    disable_web_page_preview=True,
                )
        else:
            own = False
    except:
        own = False
        sent_own_message = ""
    try:
        message_ids_str = ""
        message_ids_own_str = ""
        for message in (await bot.get_messages(chat_id=editable.chat.id, message_ids=message_ids)):
            if own :
                sent_own_message = await forward_to_own_channel(bot, message, editable, DB_OWN_CHANNEL)
            sent_message = await forward_to_channel(bot, message, editable)
            if sent_message is None:
                continue
            message_ids_str += f"{str(sent_message.id)} "
            if own :
                message_ids_own_str += f"{str(sent_own_message.id)} "
            await asyncio.sleep(3)
        SaveMessage = await bot.send_message(
            chat_id=Config.DB_CHANNEL,
            text=message_ids_str,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Owner", url ="https://telegram.me/rushidhar1999")
            ]])
        )
        try:
            Own_SaveMessage = await bot.send_message(
                chat_id=DB_OWN_CHANNEL,
                text=message_ids_own_str,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("Owner", url ="https://telegram.me/rushidhar1999")
                ]])
            )
        except:
            Own_SaveMessage = False
        if Own_SaveMessage:
            website = f"Rushidhar_{str_to_b64(str(DB_OWN_CHANNEL))}_{str_to_b64(str(Own_SaveMessage.id))}_{str_to_b64(str(SaveMessage.id))}"
        else:
            website = f"Rushidhar_{str_to_b64(str(SaveMessage.id))}"
        # share_link = f"{Config.REDIRECT_WEBSITE}/secured?start={quote_plus(encode_string(website))}"
        # share_link = f'https://telegram.me/Rushidhar_S13_1999_bot?start={website}'
        share_link = f"{Config.REDIRECT_WEBSITE}/{website}"
        await editable.edit(
            f"**Batch Files Stored in my Database!**\n\nHere is the Permanent Link of your files: {share_link} \n\n"
            f"Just Click the link to get your files!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Open Link", url=share_link)]]
            ),
            disable_web_page_preview=True
        )
        await bot.send_message(
            chat_id=int(Config.LOG_CHANNEL),
            text=f"#BATCH_SAVE:\n\nUser Full Name : {editable.reply_to_message.from_user.first_name} {editable.reply_to_message.from_user.last_name if editable.reply_to_message.from_user.last_name else ''}\nUser Name : {editable.reply_to_message.from_user.mention}\nUser ID : {editable.reply_to_message.from_user.id}\nGot Batch Link!",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open Link", url=share_link)]])
        )
    except Exception as err:
        await editable.edit(f"Something Went Wrong!\n\n**Error:** `{err}`")
        await bot.send_message(
            chat_id=int(Config.LOG_CHANNEL),
            text=f"#ERROR_TRACEBACK:\nGot Error from `{str(editable.chat.id)}` !!\n\n**Traceback:** `{err}`",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Owner", url ="https://telegram.me/rushidhar1999")]
                ]
            )
        )


async def save_media_in_channel(bot: Client, editable: Message, message: Message):
    try:
        try:
            DB_OWN_CHANNEL = await db.exist_channel_id(message.from_user.id)
            if DB_OWN_CHANNEL:
                try:
                    bot_status = await bot.get_chat_member(DB_OWN_CHANNEL, int(Config.BOT_ID))
                    user = await bot.get_chat_member(DB_OWN_CHANNEL, message.from_user.id)
                    if not (bot_status.privileges.can_post_messages and str(user.status) in ["ChatMemberStatus.ADMINISTRATOR", "ChatMemberStatus.CREATOR", "ChatMemberStatus.OWNER"]):
                        await bot.send_message(
                            chat_id=int(message.chat.id),
                            text=f"<b>⚠️ You Should Be Admin In Channel_ID, Make Bot Admin And Give Post Messages Permission For Bot In Channel_ID, The Link Now Generated Was Not From Your Channel_ID ⚠️</b>",
                            disable_web_page_preview=True,
                        )
                except:
                    await bot.send_message(
                        chat_id=int(message.chat.id),
                        text=f"<b>⚠️ You Should Be Admin In Channel_ID, Make Bot Admin And Give Post Messages Permission For Bot In Channel_ID, The Link Now Generated Was Not From Your Channel_ID ⚠️</b>",
                        disable_web_page_preview=True,
                    )
            forwarded_own_msg = await message.forward(DB_OWN_CHANNEL)
            file_er_own_id = str(forwarded_own_msg.id)
        except:
            DB_OWN_CHANNEL = ""
            file_er_own_id = ""
        forwarded_msg = await message.forward(Config.DB_CHANNEL)
        file_er_id = str(forwarded_msg.id)
        if DB_OWN_CHANNEL and file_er_own_id:
            website = f"Rushidhar_{str_to_b64(str(DB_OWN_CHANNEL))}_{str_to_b64(file_er_own_id)}_{str_to_b64(file_er_id)}"
        else:
            website = f"Rushidhar_{str_to_b64(file_er_id)}"
        # share_link = f"{Config.REDIRECT_WEBSITE}/secured?start={quote_plus(encode_string(website))}"
        # share_link = f'https://telegram.me/Rushidhar_S13_1999_bot?start={website}'
        share_link = f"{Config.REDIRECT_WEBSITE}/{website}"
        await forwarded_msg.reply_text(
            f"#PRIVATE_FILE:\n\nUser Full Name : {message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}\nUser Name : {message.from_user.mention}\nUser ID : {message.from_user.id}\nGot File Link!",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Open Link", url = share_link)]
                ]
            )
        )
        await editable.edit(
            "**Your File Stored in my Database!**\n\n"
            f"Here is the Permanent Link of your file: {share_link} \n\n"
            "Just Click the link to get your file!",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Open Link", url=share_link)]]
            ),
            disable_web_page_preview=True
        )
    except FloodWait as sl:
        if sl.value > 45:
            print(f"Sleep of {sl.value}s caused by FloodWait ...")
            await asyncio.sleep(sl.value)
            await bot.send_message(
                chat_id=int(Config.LOG_CHANNEL),
                text="#FloodWait:\n"
                     f"Got FloodWait of `{str(sl.value)}s` from `{str(editable.chat.id)}` !!",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("Owner", url ="https://telegram.me/rushidhar1999")]
                    ]
                )
            )
        await save_media_in_channel(bot, editable, message)
    except Exception as err:
        await editable.edit(f"Something Went Wrong!\n\n**Error:** `{err}`")
        await bot.send_message(
            chat_id=int(Config.LOG_CHANNEL),
            text="#ERROR_TRACEBACK:\n"
                 f"Got Error from `{str(editable.chat.id)}` !!\n\n"
                 f"**Traceback:** `{err}`",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Owner", url ="https://telegram.me/rushidhar1999")]
                ]
            )
        )
