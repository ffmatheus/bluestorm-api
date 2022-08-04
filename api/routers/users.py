from fastapi import APIRouter, Depends, HTTPException
from auth import AuthHandler
from schemas.users import UserSchema
from models.User import User
from sqlalchemy import desc
from sqlmodel import Session
from init import app
from database import get_db


router = APIRouter()
auth_handler = AuthHandler()


@app.post(
    '/register',
    status_code=201,
    tags=["Users"])
def register(
    user: UserSchema,
    username=Depends(auth_handler.auth_wrapper),
    db: Session = Depends(get_db)):
    """
    Register a user
    """
    exist_username = db.query(
        User
    ).filter(
        User.USERNAME == user.USERNAME
    ).first()

    if exist_username:
        raise HTTPException(
            status_code=400,
            detail='Username is taken')

    id = db.query(
        User.UUID
    ).order_by(
        desc(User.UUID)
    ).first()
    if not id:
        id = "0000"
    hashed_password = auth_handler.get_password_hash(user.PASSWORD)
    uuid_str = "USER{}" 
    uuid_number = str(id[0][-4:])
    number = '%04d' % (int(uuid_number) + 1)
    db_user = User(
        **user.dict())
    db_user.UUID = uuid_str.format(number)
    db_user.PASSWORD = hashed_password
    db.add(db_user)
    db.commit()
    return True


@app.post(
    "/login",
    tags=["Users"])
def login_user(
    user: UserSchema,
    db: Session = Depends(get_db)):
    """
    Login with a user and password
    """ 
    exist_username = db.query(
        User
    ).filter(
        User.USERNAME == user.USERNAME
    ).first()
    
    if not exist_username or (not auth_handler.verify_password(user.PASSWORD, exist_username.PASSWORD)):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(exist_username.USERNAME)
    return { 'token': token }
