import jwt
from decouple import config
from Models.models import SessionData
from fastapi import HTTPException,status,Request,Depends
from config.db_tables import User
from fastapi.responses import RedirectResponse
from functools import wraps
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi_sessions.session_verifier import SessionVerifier
from uuid import UUID
import json

# Create instances of the backend and frontend classes
# backend = InMemoryBackend[UUID, SessionData]()
# cookie_params = CookieParameters()
# cookie = SessionCookie(
#     cookie_name="session",
#     identifier="general_verifier",
#     auto_error=True,
#     secret_key=config('SECRET_KEY'),
#     cookie_params=cookie_params,
# )
backend = InMemoryBackend[UUID, SessionData]()
cookie_params = CookieParameters()


def get_user_id_from_session(request: Request):
    session_data_json = request.cookies.get("session_data")
    if session_data_json:
        session_data = json.loads(session_data_json)
        user_id = session_data.get("user_id")
        if user_id:
            return user_id
    return None

def is_logged_in(user_id: int = Depends(get_user_id_from_session)):
    if user_id:
        return user_id
    return None

# def is_logged_in(func):
#     @wraps(func)
#     async def wrapper(request: Request, *args, **kwargs):
#         session_id = request.cookies.get("session")
#         session_data_json = request.cookies.get("session_data")
#         print("Session ID:", session_id)
#         print("Session Data:", session_data_json)
#         if session_data_json:
#             session_data = json.loads(session_data_json)
#             user_id = session_data.get("user_id")
#             print("user_id:", user_id)
#             if user_id:
#                 return user_id

#         return RedirectResponse(url='/login')

#     return wrapper



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


# def is_logged_in(func):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         session_data = None
#         for arg in args:
#             if isinstance(arg, SessionData):
#                 session_data = arg
#                 break
        
#         if session_data is None or session_data.is_expired():
#             return RedirectResponse(url='/login')
        
#         return await func(*args, session_data=session_data, **kwargs)
    
#     return wrapper


# def is_logged_in(session_data: SessionData = Depends(cookie)):
#     # return RedirectResponse(url='/login')
#     print("po")
#     if session_data is None:
#         print("No session data")
#         # raise HTTPException(status_code=401, detail="Not authenticated")
#         # return "q31412"
#         raise HTTPException(status_code=307, detail="Not authenticated", headers={"Location": "/login"})
#     return session_data
