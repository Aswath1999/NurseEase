
# from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.email_utils import DefaultChecker
from pydantic import EmailStr, BaseModel
from pathlib import Path
from decouple import config
from typing import List
from Models.models import UserCreation
from fastapi_mail.errors import ConnectionErrors
from fastapi import HTTPException, status
import jwt
import markdown

# configuration = ConnectionConfig(
# MAIL_USERNAME=config('MAIL_USERNAME'),
# MAIL_PASSWORD=config('MAIL_PASSWORD'),
# MAIL_FROM=config('MAIL_FROM'),
# MAIL_PORT=int(config('MAIL_PORT')),
# MAIL_SERVER=config('MAIL_SERVER'),
# MAIL_TLS=True,
# MAIL_SSL=False,
# )

configuration = ConnectionConfig(
    MAIL_USERNAME=config('MAIL_USERNAME'),
    MAIL_PASSWORD=config('MAIL_PASSWORD'),
    MAIL_FROM=EmailStr(config('MAIL_FROM')),
    MAIL_PORT=int(config('MAIL_PORT')),
    MAIL_SERVER=config('MAIL_SERVER'),
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = False
)


async def sendmail(email: List[str],instance:UserCreation):
    print(email)
    print("sending mail")
    token_data = {
        'id': str(instance.id),
        'username': str(instance.username)
    }
    print(token_data)
    token=jwt.encode(token_data, config('SECRET_KEY'),algorithm='HS256')
    print("ok")
    template = f"""
    <!DOCTYPE html>
    <html>
        <head>
        </head>
        <body>
            <div style="display:flex; align-items: center; justify-content:center; flex-direction:column">
                <h3>Account Verification</h3>
                <br>
                <p>Thanks for creating the account. Please click on the link below:</p>
                <a href="http://localhost:8000/verification?token={token}">Verify your email here</a>
            </div>
            <p>Ignore this message if you did not register.</p>
        </body>
    </html>
"""

    message=MessageSchema(
        subject="NurseEase verification",
        recipients=email, #List of recipients
        body=template,
        subtype="html"
    )
    print("ok")
    fm = FastMail(configuration)
    try:
        print("message sending")
        await fm.send_message(message)
        print("message sent")
        return True
    except ConnectionErrors as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={'WWW-Authenticate':'Bearer' }
        )
 

# async def send_email_async(subject:str, email_to:EmailStr, body:dict,template:str):
#     message = MessageSchema(
#     subject=subject,
#     recipients= [email_to,],
#     template_body=body,
#     )
#     fm = FastMail(configuration)
#     try:
#         await fm.send_message(message, template_name=template)
#         return True
#     except ConnectionErrors as e:
#         # print(e)
#         return False
