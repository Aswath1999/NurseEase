import jwt
from decouple import config
from Models.models import UserCreation
from fastapi import HTTPException,status


async def verify_token(token:str):
    try:
        payload = jwt.decode(token,config("SECRET_KEY"),algorithm='HS256' )
        user=await UserCreation.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={'WWW-Authenticate':'Bearer' }
        )
    return user