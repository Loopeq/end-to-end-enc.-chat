from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.settings import get_settings
from app.models import User
from app.schemas import UserAuth
from app.security import hash_password, verify_password, create_access_token


settings = get_settings()
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_create_user(db: Session, user: UserAuth):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        if verify_password(user.password, db_user.hashed_password):
            return db_user
        return None
    new_user = User(username=user.username, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_or_register(db: Session, user: UserAuth):
    user_obj = get_or_create_user(db, user)
    if not user_obj:
        return None
    token = create_access_token({"sub": user_obj.username})
    return {"user": user_obj, "token": token}