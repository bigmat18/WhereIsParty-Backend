from datetime import datetime
from pydantic import UUID4, BaseModel, EmailStr
from typing import List, Union, Optional
from .organization import LocationSchema
from pydantic import constr

class OrganizationInEventSchema(BaseModel):
    name: str
    image_url: str
    instagram_link: str
    phone: str
    email: EmailStr


class EventSchema(BaseModel):
    id: Union[UUID4, None] = None
    name: str = None
    description: str = None
    
    date: datetime = None
    open_date: datetime = None
    close_date: datetime = None
    visible_date: datetime = None
    
    primary_color: Optional[constr(6)] = None
    secondary_color: Optional[constr(6)] = None
    
    image_url: Union[str, None] = None
    location: Union[LocationSchema, UUID4] = None
    organization: Union[OrganizationInEventSchema, None] = None
    
    class Config:
        orm_config = True