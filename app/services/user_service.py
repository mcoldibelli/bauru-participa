from database.models import User
from database.database import db


class UserService:
    @classmethod
    def create_user(cls, name: str) -> User:
        try:
            new_user = User(name=name.strip())

            db.session.add(new_user)
            db.session.commit()
            return new_user

        except Exception as e:
            raise Exception(f"Failed to create user: {str(e)}")