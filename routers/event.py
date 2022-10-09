from fastapi import APIRouter, Depends, status, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from schemas.event import EventSchema
from models import User, Organization, Event
from database import get_db
from utils.file_manager import upload_file
from utils.get_current_user import get_current_user
from .organization import get_organization


event_router = APIRouter(tags=["Event"])

@event_router.post(path="/organization/{id_organization}/events", status_code=status.HTTP_201_CREATED, response_model=EventSchema)
def event_create(id_organization: str,
                 event_data: EventSchema,
                 db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    
    organization = get_organization(id_organization, db)
    
    event = Event(event_data.name,
                  event_data.primary_color,
                  event_data.secondary_color,
                  event_data.date,
                  event_data.open_date,
                  event_data.close_date,
                  event_data.visible_date,
                  event_data.location,
                  organization.id,
                  event_data.description)
    
    db.add(event)
    db.commit()
    db.refresh(event)
    
    return event


@event_router.post(path="/event/{id_event}", status_code=status.HTTP_201_CREATED, response_model=EventSchema)
def event_update():
    pass


def event_image_update():
    pass