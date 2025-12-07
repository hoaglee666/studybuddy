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
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        # Bcrypt has a 72 byte limit - truncate if needed
        if len(password.encode('utf-8')) > 72:
            password = password[:72]
        return pwd_context.hash(password)
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not user.hashed_password:
            return None
        # Truncate password for verification too
        if len(password.encode('utf-8')) > 72:
            password = password[:72]
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        hashed_password = None
        if user.password:
            hashed_password = AuthService.get_password_hash(user.password)
        
        db_user = User(
            email=user.email,
            name=user.name,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_or_create_oauth_user(
        db: Session,
        email: str,
        name: str,
        oauth_provider: str,
        oauth_id: str,
        profile_image: str = None
    ) -> User:
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        
        if user:
            # Update OAuth info if needed
            if not user.oauth_provider:
                user.oauth_provider = oauth_provider
                user.oauth_id = oauth_id
            if profile_image and not user.profile_image:
                user.profile_image = profile_image
            db.commit()
            db.refresh(user)
            return user
        
        # Create new user
        new_user = User(
            email=email,
            name=name,
            oauth_provider=oauth_provider,
            oauth_id=oauth_id,
            profile_image=profile_image
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

auth_service = AuthService()