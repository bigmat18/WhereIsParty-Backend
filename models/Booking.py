from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from pydantic import UUID4
from sqlalchemy import Boolean, Column, String, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import JSON
from database import Base
from utils.generate_random_string import generate_random_string
from typing import Union
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
                     ForeignKey("event.id",
                                ondelete="CASCADE"))
    
    id_referral_link = Column(UUID(as_uuid=True),
                              ForeignKey("referral_link.id",
                                        ondelete="CASCADE"),
                              nullable=True)
    
    date_booked = Column(TIMESTAMP(timezone=True),
                         server_default=text('now()'))
    code = Column(String, unique=True)
    
    entered = Column(Boolean, default=False)
    
    user = relationship('User')
    referral_link = relationship('ReferralLink')
    event = relationship('Event')
    
    def __init__(self, 
                 id_user: UUID4, 
                 id_event:UUID4, 
                 id_referral_link:Union[UUID4, None] = None) -> None:
        self.id_user = id_user
        self.id_event = id_event
        self.code = generate_random_string()
        self.id_referral_link = id_referral_link