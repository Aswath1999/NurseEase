from fastapi import APIRouter, Request, Form,Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse,HTMLResponse
from Models.models import UserCreation
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from config.db import DatabaseManager
from config.db_tables import User
templates = Jinja2Templates(directory="templates")

auth= APIRouter()

@auth.get("/register")
async def register(request: Request):
    try:
       return templates.TemplateResponse("Auth/register.html", {"request": request})
    except Exception as e:
        print(e)
         

@auth.post("/register",response_class=HTMLResponse)     
async def register(request: Request,username: str = Form(...), password: str = Form(...)):
    try:
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
        return "error1"
    except ValueError as e:
        print(e)
        return "error2"
    except Exception as e:
        # return templates.TemplateResponse("error.html", {"request": request, "error_message": "Username is already taken"})
        return "error3"


