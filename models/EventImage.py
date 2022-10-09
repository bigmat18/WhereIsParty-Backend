from email.policy import default
from pydantic import UUID4
from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSON
from database import Base
import uuid


class EventImage(Base):
    __tablename__ = "event_image"
    
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    
    id_event = Column(UUID(as_uuid=True),
                      ForeignKey("event.id",
                                 ondelete="CASCADE"))
    
    image_url = Column(String)
    
    def __init__(self, id_event:UUID4, image_url:str) -> None:
        self.id_event = id_event
        self.image_url = image_url
        
        
        
class EventImageTag(Base):
    __tablename__ = "event_image_tag"
    
    id_user = Column(UUID(as_uuid=True),
                     ForeignKey("user.id",
                                ondelete="CASCADE"),
                     primary_key=True)
    
    id_image = Column(UUID(as_uuid=True),
                     ForeignKey("event_image.id",
                                ondelete="CASCADE"),
                     primary_key=True)
    
    def __init__(self, id_user:UUID4, id_image:UUID4) -> None:
        self.id_image = id_image
        self.id_user = id_user
    