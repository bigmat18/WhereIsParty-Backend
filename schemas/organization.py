from datetime import datetime
from pydantic import UUID4, BaseModel, EmailStr
from typing import List, Union
from .auth import UserSchema


class ReferralLinkSchema(BaseModel):
    id: UUID4
    name: str
    users: List[UserSchema]
    
    class Config:
        orm_mode = True


class LocationSchema(BaseModel):
    id: UUID4
    name: str
    coordinate: str
    address: str
    
    class Config:
        orm_mode = True


class OrganizationSchema(BaseModel):
    id:UUID4
    name: str
    email: EmailStr
    image_url: str
    description: Union[str, None] = None
    instragram_link: str
    phone: str
    locations: Union[List[LocationSchema], None] = None
    referral_links: Union[List[ReferralLinkSchema], None] = None
    
    class Config:
        orm_mode = True