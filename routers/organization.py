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

organization_router = APIRouter(tags=['Organization'])

@organization_router.get(path="/organization/{id_organization}", status_code=status.HTTP_200_OK)
def organization_retrieve():
    pass


def organization_update():
    pass