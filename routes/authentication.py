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


backend = InMemoryBackend[UUID, SessionData]()
cookie_params = CookieParameters()


from http.cookies import SimpleCookie

# def is_logged_in(func):
#     @wraps(func)
#     async def wrapper(request: Request, *args, **kwargs):
#         cookie = SimpleCookie(request.headers.get("cookie"))
#         session_token = cookie.get("session_token")
#         print(session_token)
#         if session_token:
#             try:
#                 decoded_token = jwt.decode(session_token.value, config("SECRET_KEY"), algorithms=["HS256"])
#                 user_id = decoded_token.get("user_id")
#                 if user_id:
#                     return await func(request, *args, **kwargs)
#             except jwt.exceptions.DecodeError:
#                 pass

#         # Store the requested URL in a cookie
#         redirect_url = request.url.path
#         response = RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)
#         # response.set_cookie(key="redirect_url", value=redirect_url)
#         return response

#     return wrapper


# def is_logged_in(func):
#     @wraps(func)
#     async def wrapper(request: Request, *args, **kwargs):
#         session_data_json = request.cookies.get("session_data")
#         if session_data_json:
#             session_data = json.loads(session_data_json)
#             user_id = session_data.get("user_id")
#             if user_id:
#                 return await func(request, *args, **kwargs)

#         # Store the requested URL in a cookie
#         redirect_url = request.url.path
#         response = RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)
#         response.set_cookie(key="redirect_url", value=redirect_url, headers=response.headers)
#         return response

#     return wrapper
def is_logged_in(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        session_data_json = request.cookies.get("session_data")
        if session_data_json:
            session_data = json.loads(session_data_json)
            user_id = session_data.get("user_id")
            if user_id:
                return await func(request, *args, **kwargs)

        # Store the requested URL in a cookie
        redirect_url = request.url.path
        response = RedirectResponse(
            url='/login',
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"}
        )
        response.set_cookie(key="redirect_url", value=redirect_url)
        return response

    return wrapper



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
