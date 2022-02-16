import motor.motor_asyncio
import datetime
from TG_ROBOT import MONGO_DB_URI


class Database:
    def init(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    async def add_chat_list(self, chat_id, ch_id=None):
        get_chat = await self.is_chat_exist(chat_id)
        if get_chat:
            chat_list = list(get_chat.get("chats"))
            if ch_id != None and int(ch_id) in chat_list:
                return True, f"{ch_id} already in white list."
            elif ch_id is not None:
                chat_list.append(int(ch_id))
                await self.col.update_one(
                    {"id": chat_id}, {"$set": {"chats": chat_list}}
                )
                return True, f"{ch_id}, added into white list"
        a_chat = {"id": int(chat_id), "chats": [ch_id]}
        await self.col.insert_one(a_chat)
        return False, " "
    
    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            notif=True,
        )
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({"id": int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users
    
    async def set_notif(self, id, notif):
        await self.col.update_one({"id": id}, {"$set": {"notif": notif}})

    async def get_notif(self, id):
        user = await self.col.find_one({"id": int(id)})
        return user.get("notif", False)

    async def get_all_notif_user(self):
        notif_users = self.col.find({"notif": True})
        return notif_users

    async def total_notif_users_count(self):
        count = await self.col.count_documents({"notif": True})
        return count

    async def delete_user(self, user_id):
        await self.col.delete_many({"id": int(user_id)})

   

    async def is_chat_exist(self, id):
        user = await self.col.find_one({"id": int(id)})
        return user if user else False

    async def get_chat_list(self, chat_id):
        get_chat = await self.is_chat_exist(chat_id)
        if get_chat:
            return get_chat.get("chats", [])
        else:
            return False
        

    async def del_chat_list(self, chat_id, ch_id=None):
        get_chat = await self.is_chat_exist(chat_id)
        if get_chat:
            chat_list = list(get_chat.get("chats"))
            if ch_id != None and ch_id in chat_list:
                chat_list.remove(int(ch_id))
                await self.col.update_one(
                    {"id": chat_id}, {"$set": {"chats": chat_list}}
                )
                return True, f"{ch_id}, removed from white list"
            elif int(ch_id) not in chat_list:
                return True, f"{ch_id}, not found in white list."
            


remdb = Database(MONGO_DB_URI, "whitelist_chats")