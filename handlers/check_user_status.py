# (c) Mr. Vishal & @AbirHasan2005 @PredatorHackerzZ

import datetime
from configs import Config
from handlers.database import Database

db = Database(Config.DATABASE_URL, Config.BOT_USERNAME)


async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id
    if not await db.is_user_exist(chat_id):
        await db.add_user(chat_id)
        await bot.send_message(
            int(Config.LOG_CHANNEL),
            f"#NEW_USER:\n\nUser Full Name : {cmd.from_user.first_name} {cmd.from_user.last_name if cmd.from_user.last_name else ''}\nUser Name : {cmd.from_user.mention}\nUser ID : {cmd.from_user.id}\nstarted @{Config.BOT_USERNAME} !!"
        )

    ban_status = await db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (
                datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await db.remove_ban(chat_id)
        else:
            await cmd.reply_text("You are Banned!.. Contact @rushidhar1999 😝", quote=True)
            return
    await cmd.continue_propagation()
