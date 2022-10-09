from datetime import datetime
from pydantic import UUID4, BaseModel, EmailStr
from typing import Union
from .organization import UserSchema, ReferralLinkSchema


class BookingSchema(BaseModel):
    id: UUID4 = None
    user: UserSchema = None
    id_event: UUID4 = None
    referral_link: ReferralLinkSchema | None = None
    date_booked: datetime = None
    code: str = None
    
    class Config:
        orm_mode = True