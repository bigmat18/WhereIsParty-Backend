from sqlalchemy.sql.expression import text
from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base
from pydantic import EmailStr, UUID4
from sqlalchemy.ext.hybrid import hybrid_property
from database import SessionLocal
from models.Location import Location
from models.ReferralLink import ReferralLink
from models.Role import Role
import uuid


class Organization(Base):
    __tablename__ = "organization"
    
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    
    name = Column(String,
                  unique=True)
    
    email = Column(String, unique=True)
    
    id_creator = Column(UUID(as_uuid=True), 
                        ForeignKey("user.id", 
                                  ondelete="CASCADE"))
    
    image_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))
    
    instagram_link = Column(String)
    
    phone = Column(String(10))
    
    def __init__(self, name:str, email:EmailStr, id_creator:UUID4, 
                 image_url:str=None, description:str=None) -> None:
        self.name = name
        self.email = email
        self.id_creator = id_creator
        self.description = description
        self.image_url = image_url
        
    @hybrid_property
    def locations(self):
        db = SessionLocal()
        return db.query(Location)\
                 .filter(Location.id_organization == self.id)\
                 .all()
                 
    @hybrid_property
    def referral_links(self):
        db = SessionLocal()
        return db.query(ReferralLink)\
                 .filter(ReferralLink.id_organization == self.id)\
                 .all()
        
        
        
class UserInOrganization(Base):
    __tablename__ = "user_in_organization"
    
    id_organization = Column(UUID(as_uuid=True),
                             ForeignKey("organization.id",
                                        ondelete="CASCADE"),
                             primary_key=True)
    
    id_user = Column(UUID(as_uuid=True),
                    ForeignKey("user.id",
                                ondelete="CASCADE"),
                    primary_key=True)
    
    id_role = Column(UUID(as_uuid=True),
                    ForeignKey("role.id",
                                ondelete="CASCADE"))
    
    def __init__(self, id_organization:UUID4, id_user:UUID4, id_role:UUID4) -> None:
        self.id_organization = id_organization
        self.id_user = id_user
        self.id_role = id_role
        