from sqlalchemy.sql.expression import text
from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base
import uuid

class ReferralLink(Base):
    __tablename__ = "referral_link"
    
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    
    id_organization = Column(UUID(as_uuid=True),
                             ForeignKey("organization.id",
                                        ondelete=True))
    
    name = Column(String)
    
    def __init__(self, name:str, id_organization:str) -> None:
        self.name = name
        self.id_organization = id_organization
    