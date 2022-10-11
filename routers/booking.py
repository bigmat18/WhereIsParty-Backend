from fastapi import APIRouter, Depends, Response, status, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from schemas.booking import BookingSchema
from models import User, Booking, ReferralLink
from database import get_db
from utils.file_manager import upload_file
from utils.get_current_user import get_current_user
from typing import Union
from sqlalchemy import and_
from .event import get_event
from typing import List

booking_router = APIRouter(tags=["Booking"])


def get_booking(id:str, db:Session) -> Booking:
    booking = db.query(Booking).filter(Booking.id == id).first()
    if not booking: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Non esiste una booking con questo id")
    return booking


@booking_router.get(path="/event/{id_event}/booking", status_code=status.HTTP_200_OK, response_model=List[BookingSchema])
def booking_list(id_event: str,
                 referral_link: str = None,
                 user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    
    event = get_event(id_event, db)
    
    if referral_link:
        referral_link = db.query(ReferralLink)\
                          .filter(and_(ReferralLink.name == referral_link, ReferralLink.id_organization == event.id_organization))\
                          .first()
        if referral_link:
            bookings = db.query(Booking).filter(and_(Booking.id_event == id_event, Booking.id_referral_link == referral_link.id)).all()
        else: 
            bookings = db.query(Booking).filter(Booking.id_event == id_event).all()
    else:
        bookings = db.query(Booking).filter(Booking.id_event == id_event).all()
    
    return bookings


@booking_router.post(path="/event/{id_event}/booking", status_code=status.HTTP_201_CREATED, response_model=BookingSchema)
def booking_create(id_event: str,
                   booking: BookingSchema,
                   user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    event = get_event(id_event, db)
    
    if booking.referral_link:
        referral_link = db.query(ReferralLink)\
                        .filter(and_(ReferralLink.name == booking.referral_link, ReferralLink.id_organization == event.id_organization))\
                        .first()
        if referral_link:
            booking = Booking(id_user=user.id, id_event=event.id, id_referral_link=referral_link.id)
        else: 
            booking = Booking(id_user=user.id, id_event=event.id)
    else:
        booking = Booking(id_user=user.id, id_event=event.id)
    
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
    
    
   
@booking_router.post(path="/booking/{id_booking}/entered", status_code=status.HTTP_200_OK, response_model=BookingSchema)
def booking_user_entered(id_booking: str,
                         user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    booking = get_booking(id_booking, db)
    
    booking.entered = True
    
    db.commit()
    db.refresh(booking)
    
    return booking