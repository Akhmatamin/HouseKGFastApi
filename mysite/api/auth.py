from fastapi import APIRouter, HTTPException, Depends
from mysite.database.db import SessionLocal
from mysite.database.models import UserProfile,RefreshToken
from mysite.database.schema import UserSchema, UserCreate,UserLoginSchema
from sqlalchemy.orm import Session
from typing import List, Optional
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from mysite.config import (SECRET_KEY,ALGORITHMS,ACCESS_TOKEN,REFRESH_TOKEN)
from datetime import datetime,timedelta
import hashlib

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


def get_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=20))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHMS[0])
    return encoded_jwt

def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=10))


@auth_router.post("/register", response_model=dict)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user_data.username).first()
    phonenumber_db = db.query(UserProfile).filter(UserProfile.phone_number == user_data.phone_number).first()
    if user_db or phonenumber_db:
        raise HTTPException(status_code=400, detail="Username or phone number already registered")

    hashed_password = get_password(user_data.password)
    user = UserProfile(
        username=user_data.username,
        password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone_number=user_data.phone_number,
        role=user_data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'message': 'User registered'}


@auth_router.post('/login',response_model=dict)
async def login(user_data: UserLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user_data.username).first()
    if not user_db or not verify_password(user_data.password, user_db.password):
        raise HTTPException(status_code=401, detail="Username or password are not correct")

    access_token = create_access_token({'sub':user_db.username})
    refresh_token = create_refresh_token({'sub': user_db.username})

    new_token= RefreshToken(
        user_id=user_db.id,
        token=refresh_token,
    )
    db.add(new_token)
    db.commit()

    return {'access_token': access_token, 'refresh_token': refresh_token,'type':'bearer','message': 'Login Successful'}

@auth_router.post('/logout',response_model=dict)
async def logout(refresh_token:str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token==refresh_token).first()
    if stored_token is None:
        raise HTTPException(status_code=401, detail="Refresh Token is invalid")

    db.delete(stored_token)
    db.commit()

    return {'message': 'Logout Successful'}


@auth_router.post('/refresh', response_model=dict)
async def refresh(refresh_token:str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token==refresh_token).first()
    if stored_token is None:
        raise HTTPException(status_code=401, detail="Refresh Token is invalid")

    access_token = create_access_token({'sub': stored_token.user_id})
    return {'access_token': access_token, 'type':'bearer'}
