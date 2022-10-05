from datetime import datetime
from pydantic import UUID4, BaseModel, EmailStr
from typing import List, Union
from .organization import LocationSchema

class OrganizationInEventSchema(BaseModel):
    name: str
    image_url: str
    instagram_link: str
    phone: str
    email: EmailStr


class EventSchema(BaseModel):
    id: UUID4
    name: str
    description: str
    date: datetime
    open_date: datetime
    close_date: datetime
    visible_date: datetime
    image_url: str
    location: LocationSchema
    organization: OrganizationInEventSchema
    
    class Config:
        orm_config = True