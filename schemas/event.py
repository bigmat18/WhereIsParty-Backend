from datetime import datetime
from pydantic import UUID4, BaseModel, EmailStr
from typing import List, Union, Optional
from .organization import LocationSchema
from pydantic import constr

class OrganizationInEventSchema(BaseModel):
    name: str
    image_url: Union[str, None]
    instagram_link: Union[str, None]
    phone: Union[str, None]
    email: EmailStr
    
    class Config:
        orm_mode = True


class EventSchema(BaseModel):
    id: Union[UUID4, None] = None
    name: str = None
    description: str = None
    
    date: datetime = None
    open_date: datetime = None
    close_date: datetime = None
    visible_date: datetime = None
    
    primary_color: str = None 
    secondary_color: str = None
    
    image_url: Union[str, None]
    location: Union[str, LocationSchema]
    organization: Union[OrganizationInEventSchema, None]
    
    class Config:
        orm_mode = True