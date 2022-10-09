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
    name: str
    description: str
    
    date: datetime
    open_date: datetime
    close_date: datetime
    visible_date: datetime
    
    primary_color: Optional[constr(6)]
    secondary_color: Optional[constr(6)]
    
    image_url: Union[str, None] = None
    location: Union[LocationSchema, UUID4]
    organization: Union[OrganizationInEventSchema, None] = None
    
    class Config:
        orm_config = True