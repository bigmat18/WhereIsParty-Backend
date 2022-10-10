from datetime import datetime
from pydantic import UUID4, BaseModel, EmailStr
from typing import Union
from .organization import UserSchema, ReferralLinkSchema
from .event import EventSchema

class BookingSchema(BaseModel):
    id: UUID4 = None
    user: UserSchema = None
    event: EventSchema = None
    referral_link: ReferralLinkSchema | None = None
    date_booked: datetime = None
    code: str = None
    
    class Config:
        orm_mode = True