from datetime import datetime
from pydantic import UUID4, BaseModel, EmailStr
from typing import List, Union, Optional
from .auth import UserSchema
from pydantic import constr


class ReferralLinkSchema(BaseModel):
    id: UUID4
    name: str = None
    users: List[Union[str, UserSchema]] = None
    
    class Config:
        orm_mode = True


class LocationSchema(BaseModel):
    id: Union[UUID4, None] = None
    name: str = None
    latitude: float = None
    longitude: float = None
    address: str = None
    
    class Config:
        orm_mode = True


class OrganizationSchema(BaseModel):
    id: Union[UUID4, None] = None
    name: str = None
    email: EmailStr = None
    image_url: Union[str, None]
    description: Union[str, None] = None
    instragram_link: Union[str, None]
    phone: Optional[constr(max_length=64)]
    locations: List[LocationSchema] = []
    referral_links: List[ReferralLinkSchema] = []
    
    class Config:
        orm_mode = True