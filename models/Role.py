from pydantic import UUID4
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base
import uuid

class Role(Base):
    __tablename__ = "role"
    
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    
    name = Column(String)
    
    id_organization = Column(UUID(as_uuid=True),
                             ForeignKey("organization.id",
                                        ondelete="CASCADE"))
    
    is_viewer = Column(BOOLEAN, default=False)
    is_editor = Column(BOOLEAN, default=False)
    is_scanner = Column(BOOLEAN, default=False)
    is_media_manager = Column(BOOLEAN, default=False)
    
    def __init__(self, 
                 name:str, 
                 id_organization:UUID4) -> None:
        self.name = name
        self.id_organization = id_organization
    