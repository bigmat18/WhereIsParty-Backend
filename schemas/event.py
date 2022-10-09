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
    name: str | None = None
    description: str | None = None
    
    date: datetime | None = None
    open_date: datetime | None = None
    close_date: datetime | None = None
    visible_date: datetime | None = None
    
    primary_color: Optional[constr(max_length=8)] | None = None
    secondary_color: Optional[constr(max_length=8)] | None = None
    
    image_url: Union[str, None] = None
    location: Union[str, LocationSchema, None] = None
    organization: Union[OrganizationInEventSchema, None] = None
    
    class Config:
        orm_config = True