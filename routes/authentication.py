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
from uuid import UUID, uuid4


# Create instances of the backend and frontend classes
backend = InMemoryBackend[UUID, SessionData]()
cookie_params = CookieParameters()
cookie = SessionCookie(
    cookie_name="session",
    identifier="general_verifier",
    auto_error=True,
    secret_key=config('SECRET_KEY'),
    cookie_params=cookie_params,
)
# Create a session verifier class
class UserVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(self, backend: InMemoryBackend[UUID, SessionData]):
        self._backend = backend

    @property
    def backend(self):
        return self._backend

    @backend.setter
    def backend(self, backend):
        self._backend = backend

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True

verifier = UserVerifier(backend=backend)

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



# Decorator function to check if the user is logged in
def is_logged_in(session_data: SessionData = Depends(verifier)):
    if session_data is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
