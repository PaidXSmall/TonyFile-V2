# (c) @TeleRoidGroup || @PredatorHackerzZ

import os
import asyncio
import traceback
from binascii import (
    Error
)
from pyrogram import (
    Client,
    enums,
    filters
)
from pyrogram.errors import (
    UserNotParticipant,
    FloodWait,
    QueryIdInvalid
)
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message
)
from configs import Config
from handlers.database import db
from handlers.add_user_to_db import add_user_to_database
from handlers.send_file import send_media_and_reply
from handlers.helpers import b64_to_str, str_to_b64
from handlers.check_user_status import handle_user_status
from handlers.force_sub_handler import handle_force_sub
from handlers.broadcast_handlers import main_broadcast_handler
from handlers.save_media import (
    save_media_in_channel,
    save_batch_media_in_channel
)
import requests
import threading

MediaList = {}

Bot = Client(
    name=Config.BOT_USERNAME,
    in_memory=True,
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

async def auto_delete_thread(bot, msg):
    await asyncio.sleep(120)
    return await bot.delete_messages(msg.chat.id, msg.id)


@Bot.on_message(filters.private)
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)


@Bot.on_message(filters.command("start") & filters.private)
async def start(bot: Client, cmd: Message):

    if cmd.from_user.id in Config.BANNED_USERS:
        await cmd.reply_text("Sorry, You are banned.")
        return

    if await handle_force_sub(bot, cmd):
        return
    
    usr_cmd = cmd.text.split("_", 1)[-1]
    if usr_cmd == "/start":
        await add_user_to_database(bot, cmd)
        await cmd.reply_text(
            Config.HOME_TEXT.format(cmd.from_user.first_name, cmd.from_user.id),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("About Bot", callback_data="aboutbot"),
                        InlineKeyboardButton("About Dev", callback_data="aboutdevs"),
                        InlineKeyboardButton("Close 🚪", callback_data="closeStartMessage")
                    ],
                    [
                        InlineKeyboardButton("Source Codes of Bot", url="https://github.com/PredatorHackerzZ/TG-FileStore")
                    ]
                ]
            )
        )
    else:
        try:
            try:
                file_id = int(b64_to_str(usr_cmd.split("_")[-2]))
            except (Error, UnicodeDecodeError):
                file_id = int(usr_cmd.split("_")[-2])
            try:
                USER_CUSTOM_DB = int(b64_to_str(usr_cmd.split("_")[-3]))
            except (Error, UnicodeDecodeError):
                USER_CUSTOM_DB = int(usr_cmd.split("_")[-3])
            GetMessage = await bot.get_messages(chat_id=USER_CUSTOM_DB, message_ids=file_id)
            own_file = True
            try:
                from_main_db_id = vars(GetMessage).get('empty')
                if from_main_db_id:
                    own_file = False
            except:
                pass
            if not own_file :
                raise Exception("Force entering except block")
        except:
            usr_cmd = cmd.text.split("_")[-1]
            try:
                file_id = int(b64_to_str(usr_cmd).split("_")[-1])
            except (Error, UnicodeDecodeError):
                file_id = int(usr_cmd.split("_")[-1])
            GetMessage = await bot.get_messages(chat_id=Config.DB_CHANNEL, message_ids=file_id)
            own_file = False
        try:
            message_ids = []
            if GetMessage.text:
                message_ids = GetMessage.text.split(" ")
                _response_msg = await cmd.reply_text(
                    text=f"**Total Files:** `{len(message_ids)}`",
                    quote=True,
                    disable_web_page_preview=True
                )
                try:
                    delete = threading.Thread(
                        target=lambda: asyncio.run(auto_delete_thread(bot, _response_msg))
                    )
                    delete.start()
                except: pass
            else:
                message_ids.append(int(GetMessage.id))
            for i in range(len(message_ids)):
                if own_file :
                    await send_media_and_reply(bot, USER_CUSTOM_DB, user_id=cmd.from_user.id, file_id=int(message_ids[i]))
                else:
                    await send_media_and_reply(bot, Config.DB_CHANNEL, user_id=cmd.from_user.id, file_id=int(message_ids[i]))
            try:
                sent_all_files = await cmd.reply_text(
                    f"**Files will be Deleted After 2 min ⏰**\n",
                    disable_web_page_preview=True, quote=True)
                delete = threading.Thread(
                    target=lambda: asyncio.run(auto_delete_thread(bot, sent_all_files))
                )
                delete.start()
            except: pass
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")


@Bot.on_message(filters.command("channel_id") & filters.private)
async def main(bot: Client, message: Message):

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    if await handle_force_sub(bot, message):
        return
    
    await add_user_to_database(bot, message)

    if message.reply_to_message:
        user_message = message.reply_to_message.text.strip()
    else:
        user_message = message.text.split(" ")[-1].strip()

    try:
        if user_message == "/channel_id":
            await message.reply_text(
                f"Send File Store Channel ID Remember Only One Channel ID Works\n\nExample:\n<code>/channel_id -100</code>xxxx",
                disable_web_page_preview=True,
                quote=True,
            )
        elif not user_message.startswith("-100"):
            await message.reply_text(
                f"Channel ID Should Starts With -100\n\nExample:\n<code>/channel_id -100</code>xxxx",
                disable_web_page_preview=True,
                quote=True,
            )
        elif user_message.startswith("-100"):
            user_message = int(user_message)
            await db.channel_id(message.from_user.id, user_message)
            await message.reply_text(
                f"User Full Name : {message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}\nUser Name : {message.from_user.mention}\nUser ID : {message.from_user.id}\nChannel ID : <code>{user_message}</code>\n<b>⚠️ You Should Be Admin In Channel_ID, Make Bot Admin And Give Post Messages Permission For Bot In Channel_ID ⚠️</b>",
                disable_web_page_preview=True,
                quote=True,
            )
            try:
                await bot.send_message(
                    chat_id=int(Config.LOG_CHANNEL),
                    text=f"User Full Name : {message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}\nUser Name : {message.from_user.mention}\nUser ID : {message.from_user.id}\nChannel ID : <code>{user_message}</code>",
                    disable_web_page_preview=True,
                )
            except: pass

    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/rushidhar1999'>CLICK HERE FOR SUPPORT </a></b> \n\n {e}",
            disable_web_page_preview=True,
        )

@Bot.on_message(filters.command("del_channel_id") & filters.private)
async def main(bot: Client, message: Message):

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    if await handle_force_sub(bot, message):
        return
    
    await add_user_to_database(bot, message)

    result = await db.del_channel_id(message.from_user.id)

    try:
        if result:
            await message.reply_text(
                f"channel_id successfully deleted",
                disable_web_page_preview=True,
                quote=True,
            )
        else:
            await message.reply_text(
                f"you didn't save any channel_id, send command /view_channel_id check you have stored any channel_id or not.",
                disable_web_page_preview=True,
                quote=True,
            )
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/rushidhar1999'>CLICK HERE FOR SUPPORT </a></b> \n\n {e}",
            disable_web_page_preview=True,
        )

@Bot.on_message(filters.command("view_channel_id") & filters.private)
async def main(bot: Client, message: Message):

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    if await handle_force_sub(bot, message):
        return
    
    await add_user_to_database(bot, message)

    result = await db.exist_channel_id(message.from_user.id)

    try:
        if result:
            await message.reply_text(
                f"User Full Name : {message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}\nUser Name : {message.from_user.mention}\nUser ID : {message.from_user.id}\nChannel ID : <code>{result}</code>\n<b>⚠️ You Should Be Admin In Channel_ID, Make Bot Admin And Give Post Messages Permission For Bot In Channel_ID ⚠️</b>",
                disable_web_page_preview=True,
                quote=True,
            )
        else:
            await message.reply_text(
                f"you didn't save any channel_id.",
                disable_web_page_preview=True,
                quote=True,
            )
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/rushidhar1999'>CLICK HERE FOR SUPPORT </a></b> \n\n {e}",
            disable_web_page_preview=True,
        )

@Bot.on_message(filters.command("shortener_api") & filters.private)
async def main(bot: Client, message: Message):

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    if await handle_force_sub(bot, message):
        return
    
    await add_user_to_database(bot, message)

    if message.reply_to_message:
        user_message = message.reply_to_message.text.strip()
    else:
        user_message = message.text.split()[-1].strip()

    user_message = user_message.split("&url=")[0]+"&url="

    try:
        if user_message.startswith("https") and "?" in user_message and "api=" in user_message and "&url=" in user_message:
            await db.shortener_api(message.from_user.id, user_message)
            await message.reply_text(
                f"User Full Name : {message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}\nUser Name : {message.from_user.mention}\nUser ID : {message.from_user.id}\nShortener Api : <code>{user_message}</code>",
                disable_web_page_preview=True,
                quote=True,
            )
            try:
                await bot.send_message(
                    chat_id=int(Config.LOG_CHANNEL),
                    text=f"User Full Name : {message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}\nUser Name : {message.from_user.mention}\nUser ID : {message.from_user.id}\nShortener Api : <code>{user_message}</code>",
                    disable_web_page_preview=True,
                )
            except: pass
        else:
            await message.reply_text(
                f"Go To Your Shortener Daseboard\nGoto Settings > Tools > Developers API\nIn That Find This https://YourShortenerWebsite.com/api?api=xxxxx&url= And Copy\n\nExample:\n<code>/shortener_api </code>https://YourShortenerWebsite.com/api?api=xxxxx&url=",
                disable_web_page_preview=True,
                quote=True,
            )
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/rushidhar1999'>CLICK HERE FOR SUPPORT </a></b> \n\n {e}",
            disable_web_page_preview=True,
        )

@Bot.on_message(filters.command("del_shortener_api") & filters.private)
async def main(bot: Client, message: Message):

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    if await handle_force_sub(bot, message):
        return
    
    await add_user_to_database(bot, message)

    result = await db.del_shortener_api(message.from_user.id)

    try:
        if result:
            await message.reply_text(
                f"shortener_api successfully deleted",
                disable_web_page_preview=True,
                quote=True,
            )
        else:
            await message.reply_text(
                f"you didn't save any shortener_api, send command /view_shortener_api check you have stored any shortener_api or not.",
                disable_web_page_preview=True,
                quote=True,
            )
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/rushidhar1999'>CLICK HERE FOR SUPPORT </a></b> \n\n {e}",
            disable_web_page_preview=True,
        )

@Bot.on_message(filters.command("view_shortener_api") & filters.private)
async def main(bot: Client, message: Message):

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    if await handle_force_sub(bot, message):
        return
    
    await add_user_to_database(bot, message)

    result = await db.exist_shortener_api(message.from_user.id)

    try:
        if result:
            await message.reply_text(
                f"User Full Name : {message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}\nUser Name : {message.from_user.mention}\nUser ID : {message.from_user.id}\nShortener Api : <code>{result}</code>",
                disable_web_page_preview=True,
                quote=True,
            )
        else:
            await message.reply_text(
                f"you didn't save any shortener_api.",
                disable_web_page_preview=True,
                quote=True,
            )
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/rushidhar1999'>CLICK HERE FOR SUPPORT </a></b> \n\n {e}",
            disable_web_page_preview=True,
        )

@Bot.on_message(filters.command("generate") & filters.private)
async def main(bot: Client, message: Message):

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    if await handle_force_sub(bot, message):
        return
    
    await add_user_to_database(bot, message)

    result = await db.exist_shortener_api(message.from_user.id)
    
    try:
        if result:
    
            if message.reply_to_message:
                user_message = message.reply_to_message.text.strip().split()
            else:
                user_message = message.text.strip().split()
                if len(user_message) == 1:
                    await message.reply_text(
                        f'Send /generate Command Along With The Link You Want To Shorten\n\n\nExample:\n/generate http://xx',
                        disable_web_page_preview=True,
                        quote=True,
                    )
                    return
                    
    
            shorteners_links = f"This Is Currently Experimental Feature Recheck If URL Created In Your Shortener Website Manage Links\n\nFull Name : {message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ''}\nUser Name : {message.from_user.mention}\nUser ID : {message.from_user.id}\n\nShortend Links:\n\n"
            for i in user_message:
                if "https" in i:
                    site_url = str(requests.get(f"{result}{i}&format=text").text).replace("\\","")
                    shorteners_links += f'[Original]({i}) -> [shorten]({site_url})\n\n'
    
            await message.reply_text(
                shorteners_links.strip(),
                disable_web_page_preview=True,
                quote=True,
            )
            try:
                await bot.send_message(
                    chat_id=int(Config.LOG_CHANNEL),
                    text=shorteners_links.strip(),
                    disable_web_page_preview=True,
                )
            except: pass
        else:
            await message.reply_text(
                f"you didn't save any shortener_api. To Store shortener_api\n\nExample:\n<code>/shortener_api </code>https://YourShortenerWebsite.com/api?api=xxxxx&url=",
                disable_web_page_preview=True,
                quote=True,
            )
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<i>Something went wrong</i> <b> <a href='https://telegram.me/rushidhar1999'>CLICK HERE FOR SUPPORT </a></b> \n\n {e}",
            disable_web_page_preview=True,
        )

@Bot.on_message(filters.command("link"))
async def main(bot: Client, message: Message):

    await add_user_to_database(bot, message)

    if await handle_force_sub(bot, message):
        return

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_to_message.reply_text("Sorry, You are banned!\n\nContact Me [ Rushidhar ](https://telegram.me/rushidhar1999)",
                                 disable_web_page_preview=True)
        return

    if Config.OTHER_USERS_CAN_SAVE_FILE is False:
        return

    if message.from_user.id == message.reply_to_message.from_user.id:
        try:
            kidding = message.reply_to_message.text
            if kidding:
                return await message.reply_to_message.reply_text("Stop Kidding Me Dude 😂😂, I Know It's Not Media Or Sticker.", disable_web_page_preview=True)
        except: pass
        await message.reply_to_message.reply_text(
            text="**Choose an option from below:**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Save in Batch", callback_data="addToBatchTrue")],
                [InlineKeyboardButton("Get Sharable Link", callback_data="addToBatchFalse")],
                [InlineKeyboardButton("Close Message", callback_data="closeMessage")]
            ]),
            quote=True,
            disable_web_page_preview=True
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"You Can Only Link Your Messages.",
            disable_web_page_preview=True,
        )
        
            


@Bot.on_message((filters.document | filters.photo | filters.sticker | filters.video | filters.audio) & filters.private)
async def main(bot: Client, message: Message):

    await add_user_to_database(bot, message)

    if await handle_force_sub(bot, message):
        return

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned!\n\nContact Me [ Rushidhar ](https://telegram.me/rushidhar1999)",
                                 disable_web_page_preview=True)
        return

    if Config.OTHER_USERS_CAN_SAVE_FILE is False:
        return

    await message.reply_text(
        text="**Choose an option from below:**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Save in Batch", callback_data="addToBatchTrue")],
            [InlineKeyboardButton("Get Sharable Link", callback_data="addToBatchFalse")],
            [InlineKeyboardButton("Close Message", callback_data="closeMessage")]
        ]),
        quote=True,
        disable_web_page_preview=True
    )


@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(Config.BOT_OWNER) & filters.reply)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db)


@Bot.on_message(filters.private & filters.command("status") & filters.user(Config.BOT_OWNER))
async def sts(_, m: Message):
    total_users = await db.total_users_count()
    await m.reply_text(
        text=f"**Total Users in DB:** `{total_users}`",
        quote=True
    )


@Bot.on_message(filters.private & filters.command("ban_user") & filters.user(Config.BOT_OWNER))
async def ban(c: Client, m: Message):
    
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban any user from the bot.\n\n"
            f"Usage:\n\n"
            f"`/ban_user user_id ban_duration ban_reason`\n\n"
            f"Eg: `/ban_user 1234567 28 You misused me.`\n"
            f"This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."
        try:
            await c.send_message(
                user_id,
                f"You are banned to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n"
                f"**Message from the admin**"
            )
            ban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"

        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(
            ban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Bot.on_message(filters.private & filters.command("unban_user") & filters.user(Config.BOT_OWNER))
async def unban(c: Client, m: Message):

    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban any user.\n\n"
            f"Usage:\n\n`/unban_user user_id`\n\n"
            f"Eg: `/unban_user 1234567`\n"
            f"This will unban user with id `1234567`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user {user_id}"
        try:
            await c.send_message(
                user_id,
                f"Your ban was lifted!"
            )
            unban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(
            unban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occurred! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Bot.on_message(filters.private & filters.command("banned_users") & filters.user(Config.BOT_OWNER))
async def _banned_users(_, m: Message):
    
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ''

    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"> **user_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, " \
                f"**Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s): `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await m.reply_text(reply_text, True)



@Bot.on_message(filters.private & filters.command("delete_user") & filters.user(Config.BOT_OWNER))
async def delete_id(c: Client, m: Message):

    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to delete any user from database.\n\n"
            f"Usage:\n\n`/delete_user user_id`\n\n"
            f"Eg: `/delete_user 1234567`\n"
            f"This will delete user with id `1234567`.",
            quote=True
        )
        return
    try:
        user_id = int(m.command[1])
        delete_user_text = f"User {user_id} deleted from database"
        await db.delete_user(user_id)
        await m.reply_text(
            delete_user_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occurred! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )
    


@Bot.on_message(filters.private & filters.command("clear_batch"))
async def clear_user_batch(bot: Client, m: Message):
    MediaList[f"{str(m.from_user.id)}"] = []
    await m.reply_text("Cleared your batch files successfully!")


@Bot.on_callback_query()
async def button(bot: Client, cmd: CallbackQuery): 
    cb_data = cmd.data
    if "aboutbot" in cb_data:
        await cmd.message.edit(
            Config.ABOUT_BOT_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Source Codes of Bot",
                                             url="https://github.com/PredatorHackerzZ/TG-FileStore")
                    ],
                    [
                        InlineKeyboardButton("Go Home", callback_data="gotohome"),
                        InlineKeyboardButton("About Dev", callback_data="aboutdevs")
                    ]
                ]
            )
        )

    elif "aboutdevs" in cb_data:
        await cmd.message.edit(
            Config.ABOUT_DEV_TEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Source Codes of Bot",
                                             url="https://github.com/PredatorHackerzZ/TG-FileStore")
                    ],
                    [
                        InlineKeyboardButton("About Bot", callback_data="aboutbot"),
                        InlineKeyboardButton("Go Home", callback_data="gotohome")
                    ]
                ]
            )
        )

    elif "gotohome" in cb_data:
        await cmd.message.edit(
            Config.HOME_TEXT.format(cmd.message.chat.first_name, cmd.message.chat.id),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("About Bot", callback_data="aboutbot"),
                        InlineKeyboardButton("About Dev", callback_data="aboutdevs"),
                        InlineKeyboardButton("Close 🚪", callback_data="closeStartMessage")
                    ],
                    [
                        InlineKeyboardButton("Source Codes of Bot", url="https://github.com/PredatorHackerzZ/TG-FileStore")
                    ]
                ]
            )
        )

    elif cb_data.startswith("ban_user_"):
        user_id = cb_data.split("_", 2)[-1]
        if Config.UPDATES_CHANNEL is None:
            await cmd.answer("Sorry Sir, You didn't Set any Updates Channel!", show_alert=True)
            return
        if not int(cmd.from_user.id) == Config.BOT_OWNER:
            await cmd.answer("You are not allowed to do that!", show_alert=True)
            return
        try:
            await bot.kick_chat_member(chat_id=int(Config.UPDATES_CHANNEL), user_id=int(user_id))
            await cmd.answer("User Banned from Updates Channel!", show_alert=True)
        except Exception as e:
            await cmd.answer(f"Can't Ban Him!\n\nError: {e}", show_alert=True)

    elif "closeStartMessage" in cb_data:
        await cmd.message.delete(True)

    else:
        if cmd.from_user.id == cmd.message.reply_to_message.from_user.id:
            if "addToBatchTrue" in cb_data:
                if MediaList.get(f"{str(cmd.from_user.id)}", None) is None:
                    MediaList[f"{str(cmd.from_user.id)}"] = []
                file_id = cmd.message.reply_to_message.id
                MediaList[f"{str(cmd.from_user.id)}"].append(file_id)
                await cmd.message.edit("File Saved in Batch!\n\n"
                                       "Press below button to get batch link.",
                                       reply_markup=InlineKeyboardMarkup([
                                           [InlineKeyboardButton("Get Batch Link", callback_data="getBatchLink")],
                                           [InlineKeyboardButton("Close Message", callback_data="closeMessage")]
                                       ]))
        
            elif "addToBatchFalse" in cb_data:
                await save_media_in_channel(bot, editable=cmd.message, message=cmd.message.reply_to_message)
        
            elif "getBatchLink" in cb_data:
                message_ids = MediaList.get(f"{str(cmd.from_user.id)}", None)
                if message_ids is None:
                    await cmd.answer("Batch List Empty!", show_alert=True)
                    return
                await cmd.message.edit("Please wait, generating batch link ...")
                await save_batch_media_in_channel(bot, editable=cmd.message, message_ids=message_ids)
                MediaList[f"{str(cmd.from_user.id)}"] = []
        
            elif "closeMessage" in cb_data:
                await cmd.message.delete(True)
        else:
            await cmd.answer("Link Your Own Messages!", show_alert=True)

    try:
        await cmd.answer()
    except QueryIdInvalid: pass


Bot.run()
