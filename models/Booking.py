from datetime import datetime
from pydantic import UUID4
from typing import Union
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import JSON
from database import Base
import uuid


class Booking(Base):
    __tablename__ = "booking"
    
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    
    id_user = Column(UUID(as_uuid=True),
                     ForeignKey("user.id",
                                ondelete="CASCADE"))
    
    id_event = Column(UUID(as_uuid=True),
                     ForeignKey("user.id",
                                ondelete="CASCADE"))
    
    id_referral_link = Column(UUID(as_uuid=True),
                              ForeignKey("user.id",
                                        ondelete="CASCADE"),
                              nullable=True)
    
    date_booked = Column(TIMESTAMP)
    code = Column(String)
    
    def __init__(self, id_user: UUID4, id_event:UUID4, date_booked:datetime, code:str,
                 id_referral_link:Union[UUID4, None] = None) -> None:
        self.id_user = id_user
        self.id_event = id_event
        self.date_booked = date_booked
        self.code = code
        self.id_referral_link = id_referral_link