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
from utils.generate_random_string import generate_random_string

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
    bookings = None
    
    if referral_link:
        referral_link = db.query(ReferralLink)\
                          .filter(and_(ReferralLink.name == referral_link, ReferralLink.id_organization == event.id_organization))\
                          .first()
        if referral_link:
            bookings = db.query(Booking)\
                         .filter(and_(Booking.id_event == id_event, Booking.id_referral_link == referral_link.id))\
                         .all()
    
    if not bookings:
        bookings = db.query(Booking)\
                     .filter(Booking.id_event == id_event)\
                     .all()
    
    return bookings 


@booking_router.post(path="/event/{id_event}/booking", status_code=status.HTTP_201_CREATED, response_model=BookingSchema)
def booking_create(id_event: str,
                   booking: BookingSchema,
                   user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    event = get_event(id_event, db)
    
    if db.query(Booking).filter(and_(Booking.id_user == user.id, Booking.id_event == id_event)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Prenotazione già avvenuta per questo utente")
        
    code = generate_random_string()
    while db.query(Booking).filter(and_(Booking.code == code, Booking.id_event == id_event)).first():
        code = generate_random_string()
        
    new_booking = None
    
    if booking.referral_link:
        referral_link = db.query(ReferralLink)\
                          .filter(and_(ReferralLink.name == booking.referral_link, ReferralLink.id_organization == event.id_organization))\
                          .first()
        new_booking = Booking(id_user=user.id, id_event=event.id, code=code, id_referral_link=referral_link.id)

    if not booking: 
        new_booking = Booking(id_user=user.id, id_event=event.id, code=code)
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    return booking


@booking_router.get(path="/user/booking", status_code=status.HTTP_200_OK, response_model=BookingSchema)
def booking_retrieve_logged_user(user: User = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id_user == user.id).order_by(Booking.date_booked.desc()).first()
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