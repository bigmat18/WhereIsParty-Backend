from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSON
from database import Base
import uuid


class EventTheme(Base):
    __tablename__ = "event_theme"
    
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    
    name = Column(String)
    config = Column(JSON)
    
    def __init__(self, name: str, config:object) -> None:
        self.name = name
        self.config = config