from fastapi import Depends, HTTPException, status
from database import get_db
from models.User import User
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT


def get_current_user(db: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends()):
    # check jwt token
    Authorize.jwt_required()
    
    # get id from token and check if user exts
    id_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.id == id_user).first()
    if not user: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                      detail="Errore nel caricamento dell'utente che sta richiedendo la risorsa")
    return user