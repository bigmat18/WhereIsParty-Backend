from datetime import datetime
from pydantic import UUID4, BaseModel, EmailStr
from typing import Union
from .organization import UserSchema, ReferralLinkSchema
from .event import EventSchema

class BookingSchema(BaseModel):
    id: UUID4 = None
    user: UserSchema = None
    event: EventSchema = None
    referral_link: ReferralLinkSchema | None | str = None
    date_booked: datetime = None
    code: str = None
    entered: bool = None
    
    class Config:
        orm_mode = True