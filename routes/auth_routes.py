from fastapi import APIRouter, Request, Form,Body,Depends, HTTPException,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse,HTMLResponse
from Models.models import UserCreation, SessionData
from uuid import uuid4,UUID
from sqlalchemy.exc import IntegrityError
from config.db import DatabaseManager, database_connection
from config.db_tables import User
import bcrypt
from .authentication import verify_token, is_logged_in,verifier,backend,cookie
from .email import sendmail
from sqlalchemy.orm import Session
from decouple import config
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi.responses import Response


templates = Jinja2Templates(directory="templates")

auth= APIRouter()




@auth.get("/register")
async def register(request: Request):
    try:
       return templates.TemplateResponse("Auth/register.html", {"request": request})
    except Exception as e:
        print(e)
         
         
@auth.post("/register",response_class=HTMLResponse)     
async def register(request: Request,username: str = Form(...), password: str = Form(...),email: str = Form(...),session: Session = Depends(database_connection)):
    try:
        email_check = session.query(User).filter(User.email ==email).first()
        print(email_check)
        if email_check !=None:
           print("email already in use")
           raise HTTPException(
            detail='Email is already registered',
            status_code= status.HTTP_409_CONFLICT)
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(email)
        print(password)
        user=UserCreation(username=username,password=password,email=email,id=str(uuid4()))
        print(user) 
        new_user=User(id=user.id,username=user.username,password=user.password,email=user.email)

        print(new_user)
        await sendmail([user.email], user)
        print("sucess sending email")
        # Add the user model to the session
        session.add(new_user)
            # Commit the changes to the database
        session.commit()
        return "sucess" #Add remplate later
    except IntegrityError as e:
        # return templates.TemplateResponse("error.html", {"request": request, "error_message": "Username is already taken"})
        print(e)
        return e
    except ValueError as e:
        print(e)
        return "error2"
    except Exception as e:
        print(e)
        return e


@auth.post("/login")
async def login(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(database_connection)
  
):
    try:

        # Check if the email exists in the database
        user = session.query(User).filter(User.username == username).first()
        session_id = uuid4()
        session_data = SessionData(user_id=user.id)
        await backend.create(session_id, session_data)
        if user is None:
            raise HTTPException(
                detail='Invalid email or password',
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        # Verify if the user is verified
        if not user.is_verified:
            raise HTTPException(
                detail='User is not verified',
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        # Verify the password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(
                detail='Invalid email or password',
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        # Perform additional login actions if needed
        cookie.attach_to_response(response, session_id)
        print(cookie)

        # Return a success response
        return {"message": "Login successful"}
    
    except Exception as e:
        raise HTTPException(
            detail='An error occurred during login',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@auth.get("/login")
async def register(request: Request):
    try:
       return templates.TemplateResponse("Auth/login.html", {"request": request})
    except Exception as e:
        print(e)


@auth.get("/logout")
async def logout(request: Request, response: Response):
    session_id = request.cookies.get("session")
    print(session_id)
    if session_id:
        backend.delete(session_id)
        cookie.delete_from_response(response)
        return {"message": "Logout successful"}
    else:
        raise HTTPException(status_code=400, detail="No active session")


@auth.get('/verification',response_class=HTMLResponse)
async def email_verification(request:Request,token: str,session: Session = Depends(database_connection)):
    user=await verify_token(token,session)
    if user and not user.is_verified:
        user.is_verified=True
        session.add(user)
        session.commit()
        print("sucess")
        return "suceess" # return template
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={'WWW-Authenticate':'Bearer' }
        )





# is_valid = bcrypt.checkpw(user_provided_password.encode('utf-8'), hashed_password)
# if is_valid:


# @app.get("/profile")
# async def profile(session_data: SessionData = Depends(verifier)):
#     user_id = session_data.user_id
#     # Retrieve user from the database using user_id
#     # ...
#     return {"user_id": user_id, "username": user.username}