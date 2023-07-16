from fastapi import APIRouter
from extensions import Base, url, get_session
from models.user import User
import datetime
from utills.security import get_api_key
from fastapi import Depends
from fastapi import Request

router = APIRouter()


@router.get("/users")
def get_users(api_key: str = Depends(get_api_key)):
    session = get_session()

    users = session.query(User).all()

    session.close()

    return users


@router.get("/users/{user_id}")
def get_user(user_id: str, api_key: str = Depends(get_api_key)):
    session = get_session()

    user = session.query(User).filter(User.id == user_id).first()

    session.close()

    return user


@router.put("/users/{user_id}")
async def update_user(user_id: str, request: Request, api_key: str = Depends(get_api_key)):
    session = get_session()

    user = session.query(User).filter(User.id == user_id).first()

    body = await request.json()
    
    if user is None:
        return None
    
    email = body.get('email')
    password = body.get('password')

    if email:
        user.email = email

    if password:
        user.password = password

    session.commit()
    session.close()

    return "User updated"

@router.post("/users")
async def create_user(request: Request, api_key: str = Depends(get_api_key)):
    session = get_session()

    body = await request.json()

    email = body.get('email')
    password = body.get('password')

    user = User(email=email, password=password)

    session.add(user)
    session.commit()
    session.close()

    return "User created"

@router.delete("/users/{user_id}")
def delete_user(user_id: str, api_key: str = Depends(get_api_key)):
    session = get_session()

    user = session.query(User).filter(User.id == user_id).first()

    if user is None:
        return None

    session.delete(user)
    session.commit()
    session.close()

    return "User deleted"