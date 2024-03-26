# (c) @PredatorHackerzZ || @TeleRoidGroup

import os


class Config(object):
	API_ID = int(os.environ.get("API_ID", 12411512))
	API_HASH = os.environ.get("API_HASH", "0417d4f5fa67431b3c1b984a712cdbe3")
	BOT_TOKEN = os.environ.get("BOT_TOKEN", "6749516588:AAEGOSKs1BaW6BC8a4kS1viust8l_OkABuo")
	BOT_USERNAME = os.environ.get("BOT_USERNAME", "Tony_FilesSharingbot")
	DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1001650457516"))
	BOT_OWNER = int(os.environ.get("BOT_OWNER", "907308115"))
	BOT_ID = int(os.environ.get("BOT_ID", "6749516588"))
	DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://tonyw:w@cluster0.zwgsk8r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
	UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "Tony_Files")
	UPDATES_CHANNEL_ID = os.environ.get("UPDATES_CHANNEL_ID", "-1001326077855")
	LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", -1002036323594))
	BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "12345678").split())
	FORWARD_AS_COPY = bool(os.environ.get("FORWARD_AS_COPY", False))
	BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))
	BANNED_CHAT_IDS = list(set(int(x) for x in os.environ.get("BANNED_CHAT_IDS", "").split()))
	OTHER_USERS_CAN_SAVE_FILE = bool(os.environ.get("OTHER_USERS_CAN_SAVE_FILE", True))
	REDIRECT_WEBSITE = os.environ.get("REDIRECT_WEBSITE", "https://tonyfs.kristyxx.workers.dev")
	ABOUT_BOT_TEXT = f"""
This is a Permanent FileStore Bot. 
Send Me any Media or File.I can Work In Channel too Add Me to Channel with Edit Permission, I will add save Uploaded File in Channel and Share a Shareable Link. 

╭──[ **🔅 FɪʟᴇSᴛᴏʀᴇBᴏᴛ 🔅 ** ]──⍟
│
├🔸🤖 **My Name: [Fɪʟᴇ Sᴛᴏʀᴇ Bᴏᴛ](https://telegram.me/{BOT_USERNAME}) **
│
├🔸📝 **Language: [Pʏᴛʜᴏɴ](https://www.python.org) **
│
├🔹📚 **Library: [Pʏʀᴏɢʀᴀᴍ](https://docs.pyrogram.org) **
│
├🔹📡 **Hosted On: [Mᴏɢᴇɴɪᴜs](https://mogenius.com/) **
│
├🔸👨‍💻 **Developer: [Rᴜsʜɪᴅʜᴀʀ](https://telegram.me/KristyX_TG) **
│
╰──[** 😎 🔅 [ Rᴜsʜɪᴅʜᴀʀ ] 🔅 😎 **]──⍟
"""
	ABOUT_DEV_TEXT = f"""
🧑🏻‍💻 **𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿: [Rᴜsʜɪᴅʜᴀʀ](https://telegram.me/rushidhar1999) **  

𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 𝐢𝐬 𝐒𝐮𝐩𝐞𝐫 𝐍𝐨𝐨𝐛. 𝐉𝐮𝐬𝐭 𝐋𝐞𝐚𝐫𝐧𝐢𝐧𝐠 𝐟𝐫𝐨𝐦 𝐎𝐟𝐟𝐢𝐜𝐢𝐚𝐥 𝐃𝐨𝐜𝐬. 𝐀𝐧𝐝 𝐒𝐞𝐞𝐤𝐢𝐧𝐠 𝐇𝐞𝐥𝐩 𝐅𝐫𝐨𝐦 𝐏𝐫𝐨 𝐂𝐨𝐝𝐞𝐫𝐬\n** [Rᴜsʜɪᴅʜᴀʀ](https://telegram.me/rushidhar1999) **

𝐈𝐟 𝐘𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐃𝐨𝐧𝐚𝐭𝐞 𝐎𝐮𝐫 𝐇𝐚𝐫𝐝 𝐖𝐨𝐫𝐤. 𝐘𝐨𝐮 𝐂𝐚𝐧 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐓𝐡𝐞 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫. 

𝐀𝐥𝐬𝐨 𝐫𝐞𝐦𝐞𝐦𝐛𝐞𝐫 𝐭𝐡𝐚𝐭 𝐝𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 𝐰𝐢𝐥𝐥 𝐃𝐞𝐥𝐞𝐭𝐞 𝐀𝐝𝐮𝐥𝐭 𝐂𝐨𝐧𝐭𝐞𝐧𝐭𝐬 𝐟𝐫𝐨𝐦 𝐃𝐚𝐭𝐚𝐛𝐚𝐬𝐞. 𝐒𝐨 𝐛𝐞𝐭𝐭𝐞𝐫 𝐝𝐨𝐧'𝐭 𝐒𝐭𝐨𝐫𝐞 𝐓𝐡𝐨𝐬𝐞 𝐊𝐢𝐧𝐝 𝐨𝐟 𝐓𝐡𝐢𝐧𝐠𝐬.
"""
	HOME_TEXT = """
Hello, [{}](tg://user?id={})\n\nThis is a Permanent **Fɪʟᴇ Sᴛᴏʀᴇ Bᴏᴛ**.

How to Use Bot & it's Benefits??

📢 Send me any File & It will be uploaded in My Database & You will Get the File Link.

⚠️ Benefits: If you have a TeleGram Movie Channel or Any Copyright Channel, Then Its Useful for Daily Usage, You can Send Me Your File & I will Send Permanent Link to You & Channel will be Safe from **CopyRight Infringement** Issue. I support Channel Also You Can Check **About Bot**.

❌ **PORNOGRAPHY CONTENTS** are strictly prohibited & get Permanent Ban.
"""
