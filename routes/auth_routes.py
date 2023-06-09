from fastapi import APIRouter, Request, Form,Body,Depends, HTTPException,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse,HTMLResponse
from Models.models import UserCreation, SessionData
from uuid import uuid4,UUID
from sqlalchemy.exc import IntegrityError
from config.db import database_connection
from config.db_tables import User, Patient
import bcrypt
from .authentication import verify_token,backend
from .email import sendmail
from sqlalchemy.orm import Session
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi.responses import Response
from urllib.parse import quote
import json

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
        new_user=User(username=user.username,password=user.password,email=user.email)

        print(new_user)
        await sendmail([user.email], user)
        print("sucess sending email")
        # Add the user model to the session
        session.add(new_user)
            # Commit the changes to the database
        session.commit()
        session.refresh(new_user) 
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

@auth.get("/login")
async def login(request: Request):
    try:
       return templates.TemplateResponse("Auth/login.html", {"request": request})
    except Exception as e:
        print(e)
        return e


@auth.post("/login", include_in_schema=False)
async def login_post(
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
        session_data_json = json.dumps(session_data.dict())
        
        # Set session_id and session_data as cookies
        response.set_cookie(key="session", value=session_id)
        response.set_cookie(key="session_data", value=session_data_json)
        user.is_online = True
        # Add the user model to the session
        session.add(user)
            # Commit the changes to the database
        session.commit()
        # redirect_url = request.cookies.get("redirect_url")
        # print(redirect_url)
        # if redirect_url:
        #     response.delete_cookie(key="redirect_url")
        #     print(request.cookies.get("redirect_url"))
        #     # Redirect the user back to the originally requested URL using a GET request
        #     return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)

        # Return a success response
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER,headers=response.headers)
        return {"message": "Login successful"}
    
    except Exception as e:
        print(e)
        raise HTTPException(
            detail='An error occurred during login',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




@auth.get("/logout")
async def logout(request: Request, response: Response,session: Session = Depends(database_connection)):
    session_id = request.cookies.get("session")
    session_data_json = request.cookies.get("session_data")
    session_data = json.loads(session_data_json)
    user_id = session_data.get("user_id")
    print(user_id,type(user_id))
    # session.query(Patient).filter(Patient.user_id == user_id).update({"user_id": None}) #the user_id is set to none when the patient logs out
    user = session.query(User).filter(User.id == user_id).first()
    user.is_online = False # user is set offline
    session.add(user)
    session.commit()
    
    if session_id:
        response.delete_cookie(key="session")
    
    if session_data_json:
        response.delete_cookie(key="session_data")
    
    if not session_id and not session_data_json:
        return {"message": "No active session"}
    else:
        return {"message": "Logged out successfully"}




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

