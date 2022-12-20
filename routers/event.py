from fastapi import APIRouter, Depends, status, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from schemas.event import EventSchema
from models import User, ReferralLink, Event, Location
from database import get_db
from utils.file_manager import delete_file, upload_file, AWS_BUCKET_URL
from utils.get_current_user import get_current_user
from .organization import get_organization


event_router = APIRouter(tags=["Event"])


def get_event(id:str, db:Session) -> Event:
    event = db.query(Event).filter(Event.id == id).first()
    if not event: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Non esiste una event con questo id")
    return event


@event_router.post(path="/organization/{id_organization}/events", status_code=status.HTTP_201_CREATED)
def event_create(id_organization: str,
                 event_data: EventSchema,
                 db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    
    organization = get_organization(id_organization, db)
    

    location = db.query(Location).filter(Location.id == str(event_data.location)).first()
    if not location:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Location non esistente")
    
    event = Event(event_data.name,
                  event_data.primary_color,
                  event_data.secondary_color,
                  event_data.date,
                  event_data.open_date,
                  event_data.close_date,
                  event_data.visible_date,
                  location.id,
                  organization.id,
                  event_data.description)
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    return event


@event_router.get(path="/event/{id_event}", status_code=status.HTTP_200_OK, response_model=EventSchema)
def event_retrieve(id_event: str,
                   id_referral: str = None,
                   db: Session = Depends(get_db)):
    if id_referral and db.query(ReferralLink).filter(ReferralLink.id == id_referral):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Refferal link invalido")
        
    event = get_event(id_event, db)
    
    return event

