from datetime import datetime
from pydantic import UUID3, UUID4, UUID5, BaseModel, EmailStr, UUID1
from typing import Union
from .organization import UserSchema, ReferralLinkSchema
from .event import EventSchema

class BookingSchema(BaseModel):
    id: Union[UUID4, UUID1, UUID3, UUID5] = None
    user: UserSchema = None
    event: EventSchema = None
    referral_link: Union[ReferralLinkSchema, None, str] = None
    date_booked: datetime = None
    code: str = None
    entered: bool = None
    
    class Config:
        orm_mode = True