from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..models.user import User
from ..schemas.user import UserCreate
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)