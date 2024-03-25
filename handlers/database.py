# (c) @PredatorHackerzZ

import datetime
import motor.motor_asyncio
from configs import Config


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        user = await self.col.find_one({'id': int(id)})
        return user.get('ban_status', default)

    async def get_all_banned_users(self):
        banned_users = self.col.find({'ban_status.is_banned': True})
        return banned_users

    async def channel_id(self, id, channel_id):
        await self.col.update_one({'id': int(id)}, {'$set': {'channel_id': channel_id}}, upsert=True)

    async def del_channel_id(self, id):
        id = str(id).strip()
        user = await self.col.find_one({'id': int(id)})
        if user.get('channel_id'):
            await self.col.update_one({'id': int(id)},{'$unset': {'channel_id': 1}}, upsert=True)
            return True
        else:
            return False

    async def exist_channel_id(self, id):
        user = await self.col.find_one({'id': int(id)})
        dump_id = user.get('channel_id')
        return int(dump_id) if dump_id else False

    async def shortener_api(self, id, shortener_api):
        await self.col.update_one({'id': int(id)}, {'$set': {'shortener_api': shortener_api}}, upsert=True)

    async def del_shortener_api(self, id):
        id = str(id).strip()
        user = await self.col.find_one({'id': int(id)})
        if user.get('shortener_api'):
            await self.col.update_one({'id': int(id)},{'$unset': {'shortener_api': 1}}, upsert=True)
            return True
        else:
            return False

    async def exist_shortener_api(self, id):
        user = await self.col.find_one({'id': int(id)})
        shortener_api = user.get('shortener_api')
        return shortener_api.strip() if shortener_api else False


db = Database(Config.DATABASE_URL, Config.BOT_USERNAME)
