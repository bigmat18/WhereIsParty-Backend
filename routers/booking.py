from fastapi import APIRouter, Depends, Response, status, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from schemas.booking import BookingSchema
from models import User, Booking, ReferralLink
from database import get_db
from utils.file_manager import upload_file
from utils.get_current_user import get_current_user
from typing import Union
from .referral import get_referral_link
from .event import get_event


booking_router = APIRouter(tags=["Booking"])


@booking_router.post(path="/event/{id_event}/booking", status_code=status.HTTP_201_CREATED, response_model=BookingSchema)
def booking_create(id_event: str,
                   booking: BookingSchema,
                   user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    event = get_event(id_event, db)
    
    booking = Booking(id_user=user.id, id_event=event.id, id_referral_link=booking.referral_link)
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    return booking


@booking_router.get(path="/user/booking", status_code=status.HTTP_200_OK, response_model=BookingSchema)
def booking_retrieve_logged_user(user: User = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id_user == user.id).first()
    if booking: return booking
    else: return Response(status_code=status.HTTP_200_OK)