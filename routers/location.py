from fastapi import APIRouter, Depends, status, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from models.Location import Location
from schemas.organization import LocationSchema
from models import User
from database import get_db
from utils.file_manager import upload_file
from utils.get_current_user import get_current_user
from .organization import get_organization

location_router = APIRouter(tags=["Locations"])


def get_location(id:str, db:Session) -> Location:
    location = db.query(Location).filter(Location.id == id).first()
    if not location: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Non esiste una location con questo id")
    return location


@location_router.post(path="/organization/{id_organization}/locations", status_code=status.HTTP_201_CREATED, response_model=LocationSchema)
def location_create(id_organization:str,
                    location_data: LocationSchema,
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    organization = get_organization(id_organization, db)
    
    location = Location(location_data.name,
                        location_data.longitude,
                        organization.id,
                        location_data.longitude,
                        location_data.address)
    
    db.add(location)
    db.commit()
    db.refresh(location)
    
    return location


@location_router.patch(path="/location/{id_location}", status_code=status.HTTP_200_OK, response_model=LocationSchema)
def location_update(id_location:str,
                    location_data: LocationSchema,
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    location = get_location(id_location, db)
    
    if location_data.name:
        location.name = location_data.name
        
    if location_data.latitude:
        location.latitude = location_data.latitude
        
    if location_data.longitude:
        location.longitude = location_data.longitude
        
    if location_data.address:
        location.address = location_data.address
        
    db.commit()
    db.refresh(location)
    
    return location