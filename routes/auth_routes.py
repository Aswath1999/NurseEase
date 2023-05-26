from fastapi import APIRouter, Request, Form,Body,Depends, HTTPException,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse,HTMLResponse
from Models.models import UserCreation
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from config.db import DatabaseManager, database_connection
from config.db_tables import User
import bcrypt
from fastapi.security import OAuth2PasswordRequestForm
from .authentication import verify_token
from .email import sendmail

templates = Jinja2Templates(directory="templates")

auth= APIRouter()

@auth.get("/register")
async def register(request: Request):
    try:
       return templates.TemplateResponse("Auth/register.html", {"request": request})
    except Exception as e:
        print(e)
         
         
@auth.post("/register",response_class=HTMLResponse)     
async def register(request: Request,username: str = Form(...), password: str = Form(...),email: str = Form(...),db_manager: DatabaseManager = Depends(database_connection)):
    try:
        email_check = db_manager.session.query(User).filter(User.email ==email).first()
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
        db_manager.session.add(new_user)
            # Commit the changes to the database
        db_manager.session.commit()
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
    finally:
        if db_manager:
            db_manager.close_connection()

"""
@auth.post('/login/', status_code=status.HTTP_200_OK)
# async def login(request:Request,username: str = Form(...), password: str = Form(...),db: DatabaseManager = Depends(database_connection)):
async def login(request:Request,form_data: OAuth2PasswordRequestForm = Depends(),db: DatabaseManager = Depends(database_connection)):
    # Filter search for user
    username = form_data.username
    password = form_data.password
    print(username, password)
    user = db.query(User).filter(User.username== username).first()
    if not user:
        raise HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "Invalid Username or Password",
        headers={"WWW-Authenticate":"Bearer"}
        )
    if user.is_verified != True:
        raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail= "Account Not Verified"
        )
    # access_token = create_access_token(data={'user_id':user.id})
    return {
    'access_token':access_token,
    'token_type': 'bearer'
    }
""" 
@auth.get('/verification',response_class=HTMLResponse)
async def email_verification(request:Request,token: str ):
    user=await verify_token(token)
    if user and not user.is_verified:
        user.is_verified=True
        await user.save()
        print("sucess")
        return "suceess" # return template
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={'WWW-Authenticate':'Bearer' }
        )

@auth.get("/login")
async def register(request: Request):
    try:
       return templates.TemplateResponse("Auth/login.html", {"request": request})
    except Exception as e:
        print(e)

"""
@auth.post("/register",response_class=HTMLResponse)     
async def register(request: Request,username: str = Form(...), password: str = Form(...)):
    try:
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user=UserCreation(username=username,password=password,id=str(uuid4()))
        new_user=User(id=user.id,username=user.username,password=user.password)
        connection=DatabaseManager()
        # Add the user model to the session
        connection.session.add(new_user)
        # Commit the changes to the database
        connection.session.commit()
        return "sucess"
    except IntegrityError as e:
        # return templates.TemplateResponse("error.html", {"request": request, "error_message": "Username is already taken"})
        return e
    except ValueError as e:
        print(e)
        return "error2"
    except Exception as e:
        # return templates.TemplateResponse("error.html", {"request": request, "error_message": "Username is already taken"})
        return "error3"
"""


# is_valid = bcrypt.checkpw(user_provided_password.encode('utf-8'), hashed_password)
# if is_valid: