from datetime import datetime
from typing import Union
from pydantic import UUID4
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import JSON
from database import Base
import uuid


class Event(Base):
    __tablename__ = "event"
    
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    
    name = Column(String)
    description = Column(String)
    
    date = Column(TIMESTAMP(timezone=True))
    open_date = Column(TIMESTAMP(timezone=True))
    close_date = Column(TIMESTAMP(timezone=True))
    visible_date = Column(TIMESTAMP(timezone=True))
    
    image_url = Column(String)
    
    id_location = Column(UUID(as_uuid=True),
                         ForeignKey("location.id",
                                    ondelete="CASCADE"))
    
    id_organization = Column(UUID(as_uuid=True),
                             ForeignKey("organization.id",
                                        ondelete="CASCADE"))
    
    primary_color = Column(String(6))
    secondary_color = Column(String(6))
    
    location = relationship("Location")
    organization = relationship("Organization")
    
    
    def __init__(self, 
                 name:str,
                 primary_color:str,
                 secondary_color:str, 
                 date:datetime, 
                 open_date:datetime,
                 close_date:datetime,
                 visible_date:datetime, 
                 id_location:UUID4,
                 id_organization:UUID4,
                 description:Union[str, None] = None) -> None:
        
        self.name = name
        self.description = description
        
        self.open_date = open_date
        self.close_date = close_date
        self.visible_date = visible_date
        self.date = date
        
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        
        self.id_organization = id_organization
        self.id_location = id_location
        