import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from handlers.helpers import str_to_b64
import threading

async def reply_forward(message: Message, file_id: int):
    try:
        await message.reply_text(
            f"**Files will be Deleted After 5 min ⏰**\n",
            disable_web_page_preview=True, quote=True)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await reply_forward(message, file_id)

async def media_forward(bot: Client, USER_CUSTOM_DB, user_id: int, file_id: int):
    try:
        if Config.FORWARD_AS_COPY is True:
            return await bot.copy_message(
                chat_id=user_id, from_chat_id=int(USER_CUSTOM_DB), message_id=file_id
            )
        elif Config.FORWARD_AS_COPY is False:
            return await bot.forward_messages(
                chat_id=user_id, from_chat_id=int(USER_CUSTOM_DB), message_ids=file_id
            )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return media_forward(bot, USER_CUSTOM_DB, user_id, file_id)


async def auto_delete_thread(bot, msg):
    await asyncio.sleep(2400)
    return await bot.delete_messages(msg.chat.id, msg.id)


async def send_media_and_reply(bot: Client, USER_CUSTOM_DB, user_id: int, file_id: int):
    sent_message = await media_forward(bot, USER_CUSTOM_DB, user_id, file_id)
    # await reply_forward(message=sent_message, file_id=file_id)
    await asyncio.sleep(2)
    delete = threading.Thread(
        target=lambda: asyncio.run(auto_delete_thread(bot, sent_message))
    )
    delete.start()
