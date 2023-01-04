from pydantic import UUID4
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base
from database import SessionLocal
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
import uuid

class ReferralLink(Base):
    __tablename__ = "referral_link"
    
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    
    id_organization = Column(UUID(as_uuid=True),
                             ForeignKey("organization.id",
                                        ondelete="CASCADE"))
    
    name = Column(String)
    
    def __init__(self, 
                 name:str,
                 id_organization:str) -> None:
        self.name = name
        self.id_organization = id_organization
        
    @hybrid_property
    def users(self):
        db = SessionLocal()
        user_in_referral = db.query(ReferralLinkUser)\
                             .filter(ReferralLinkUser.id_referral_link == self.id)\
                             .all()
        users = []
        for el in user_in_referral: users.append(el.user)
        
        db.close()
        return users
        
class ReferralLinkUser(Base):
    __tablename__ = "referral_link_user"
    
    id_referral_link = Column(UUID(as_uuid=True),
                              ForeignKey("referral_link.id",
                                         ondelete="CASCADE"),
                              primary_key=True)
    
    id_user = Column(UUID(as_uuid=True),
                     ForeignKey("user.id",
                                ondelete="CASCADE"),
                     primary_key=True)
    
    user = relationship("User")
    
    
    def __init__(self, 
                 id_user:UUID4, 
                 id_referral_link:UUID4) -> None:
        self.id_user = id_user
        self.id_referral_link = id_referral_link