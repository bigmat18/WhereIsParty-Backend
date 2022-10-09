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
                   id_referral: str,
                   user: User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    if db.query(ReferralLink).filter(ReferralLink.id == id_referral):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Refferal link invalido")
        
    event = get_event(id_event, db)
    
    return event


@event_router.patch(path="/event/{id_event}", status_code=status.HTTP_200_OK, response_model=EventSchema)
def event_update(id_event: str,
                 event_data: EventSchema,
                 user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    event = get_event(id_event, db)
    
    if event_data.name:
        event.name = event_data.name
        
    if event_data.description:
        event.description = event_data.description

    if event_data.date:
        event.date = event_data.date
        
    if event_data.open_date:
        event.open_date = event_data.open_date
        
    if event_data.close_date:
        event.close_date = event_data.close_date

    if event_data.visible_date:
        event.visible_date = event_data.visible_date

    if event_data.primary_color:
        event.primary_color = event_data.primary_color
        
    if event_data.secondary_color:
        event.secondary_color = event_data.secondary_color
        
    if event_data.location:
        location = db.query(Location).filter(Location.id == event_data.location).first()
        if location: event.location = location.id

    db.commit()
    db.refresh(event)

    return event


@event_router.patch(path="/event/{id_event}/image", status_code=status.HTTP_200_OK)
def event_image_update(id_event: str,
                       image: UploadFile = File(),
                       user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    
    event = get_event(id_event, db)
    
    url = upload_file(image.file, f"/event-{event.id}", "event-images")
    
    if url and event.image_url:
        path = event.image_url.replace(AWS_BUCKET_URL + "/", '')
        try: delete_file(path)
        except: print("Eliminazione vecchio file non riuscita")
        
    event.image_url = url
    db.commit()
    db.refresh(event)
        
    return {"image_url": url}