# (c) @PredatorHackerzZ

import asyncio
from typing import (
    Union
)
from configs import Config
from pyrogram import Client, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
    
async def handle_force_sub(bot: Client, cmd: Message):
    try:
        user_message = cmd.text.replace("/start ","")
        user_message = f"https://telegram.me/{Config.BOT_USERNAME}?start={user_message}"
    except: user_message = "https://telegram.me/Rushidhar1999"

    try:
        if Config.UPDATES_CHANNEL is not None:
            try:
                user = await bot.get_chat_member(Config.UPDATES_CHANNEL, cmd.from_user.id)
                if user.status == enums.ChatMemberStatus.BANNED:
                    await bot.send_message(
                        chat_id=cmd.chat.id,
                        text="Sorry Sir, You are Banned to use me. Contact me [ RUSHIDHAR ](https://t.me/rushidhar1999).",
                        disable_web_page_preview=True
                    )
                    return True
            except UserNotParticipant:
                await bot.send_message(
                    chat_id=cmd.chat.id,
                    text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use this Bot!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Join Updates Channel 🤖", url=f"https://t.me/{Config.UPDATES_CHANNEL}")
                            ],
                            [
                                InlineKeyboardButton("🔃 Refresh/Owner 🔃", url=user_message)
                            ]
                        ]
                    ),
                )
                return True
            except Exception as e:
                await bot.send_message(
                    chat_id=cmd.chat.id,
                    text=f"Something went Wrong. Contact me [ RUSHIDHAR ](https://t.me/rushidhar1999).\n{e}",
                    disable_web_page_preview=True
                )
                return True
        return False
    except FloodWait as e:
        print(f"Sleep of {e.value}s caused by FloodWait ...")
        await asyncio.sleep(e.value)
        return await handle_force_sub(bot, cmd)
