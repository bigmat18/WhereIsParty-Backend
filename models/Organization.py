from sqlalchemy.sql.expression import text
from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base
from pydantic import EmailStr, UUID4
import uuid


class Organizarion(Base):
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
    
    instagram_link = Column(String)
    
    phone = Column(String(10))
    
    def __init__(self, name:str, email:EmailStr, id_creator:UUID4, 
                 image_url:str=None, description:str=None) -> None:
        self.name = name
        self.email = email
        self.id_creator = id_creator
        self.description = description
        self.image_url = image_url