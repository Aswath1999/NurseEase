import jwt
from decouple import config
from Models.models import UserCreation
from fastapi import HTTPException,status
from config.db_tables import User




async def verify_token(token: str,session):
    try:
        print("Verifying token")
        payload = jwt.decode(token, config('SECRET_KEY'), algorithms=['HS256'])
        print(payload)

        user = session.query(User).filter(User.id == payload.get('id')).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={'WWW-Authenticate': 'Bearer'}
            )

        return user

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={'WWW-Authenticate': 'Bearer'}
        )


# async def verify_token(token:str):
#     try:
#         print("Verifying token")
#         payload = jwt.decode(token,config('SECRET_KEY'), algorithms=['HS256'] )
#         print(payload)
#         # user=await db_manager.session.query(User).filter(User.id ==payload.get('id')).first()
#         user = await User.get_by_id(db_manager.session, payload.get('id'))
#         # user=await db_manager.session.get(id=payload.get('id'))
#     except Exception as e:
#         print(e)
#     except:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="invalid token",
#             headers={'WWW-Authenticate':'Bearer' }
#         )
#     return user