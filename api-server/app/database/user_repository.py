from datetime import datetime

from app.database.base_repository import BaseRepository
from app.models.user import User, UserCreate
from app.utils.get_password_hash import get_password_hash


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__("User")

    async def create_user(self, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        user_dict = user.model_dump(exclude={"password"})
        user_dict["password"] = hashed_password
        user_dict["created_at"] = datetime.now()

        result = await self.insert_one(user_dict)
        return await self.find_one({"_id": result})
