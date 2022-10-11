from fastapi import APIRouter, Depends, status, HTTPException, Form
from sqlalchemy.orm import Session
from schemas.auth import LoginSchema, AuthenticationSchema
from models.User import User
from database import get_db
from fastapi_jwt_auth import AuthJWT
from utils.get_current_user import get_current_user
from pydantic import EmailStr,constr
from typing import Optional
from fastapi import File, UploadFile
from utils.file_manager import upload_file
import datetime


auth_router = APIRouter(tags=['Authentication'])


@auth_router.post('/login', status_code=status.HTTP_200_OK, response_model=AuthenticationSchema)
def login(credentials: LoginSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    
    # check if user exists
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"La mail {credentials.email} è errata")
        
    # check if password is correct
    if not user.check_password(credentials.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"La password è errata")
        
    # update last login and save
    user.last_login = datetime.datetime.now()
    user.access_revoked = False
    db.commit()
    
    # generate new tokens
    access = Authorize.create_access_token(subject=str(user.id))
    refresh = Authorize.create_refresh_token(subject=str(user.id))
    return {"access_token": access, "refresh_token": refresh}



@auth_router.post('/registration', status_code=status.HTTP_201_CREATED, response_model=AuthenticationSchema)
def registration(email: EmailStr = Form(), 
                 password: str = Form(), 
                 first_name: Optional[constr(max_length=64)] = Form(None), 
                 last_name: Optional[constr(max_length=64)] = Form(None),
                 image: UploadFile = File(default=None),
                 db: Session = Depends(get_db), 
                 Authorize: AuthJWT = Depends()):
    
    # check if user altredy exists
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"La mail {email} è usata da un altro utente")
    
    # create and save user
    user = User(email=email, password=password, first_name=first_name, last_name=last_name)
    user.last_login = datetime.datetime.now()
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # ulpoad file if this exits
    if image: 
        url = upload_file(image.file, f"user-{user.id}","users-images/")
        user.image_url = url
        db.commit()
        db.refresh(user)
    
    # generate tokens
    access = Authorize.create_access_token(subject=str(user.id))
    refresh = Authorize.create_refresh_token(subject=str(user.id))
    return {"access_token": access, "refresh_token": refresh}
    


@auth_router.get('/logout', status_code=status.HTTP_200_OK)
def logout(db: Session = Depends(get_db),
           user: User = Depends(get_current_user)):
    # set user logged out and save
    user.access_revoked = True
    db.commit()
    return {"msg": "Logout sucessfull"}


@auth_router.get('/token/refresh', status_code=status.HTTP_200_OK)
def refresh_token(Authorize: AuthJWT = Depends()):
    # verify refresh token
    Authorize.jwt_refresh_token_required()
    
    # get user_id and create new access token
    user_id = Authorize.get_jwt_subject()
    access = Authorize.create_access_token(subject=str(user_id))
    return {"access_token": access}