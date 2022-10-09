from sqlalchemy.sql.expression import text
from sqlalchemy import Column, String, ForeignKey, BOOLEAN, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from geoalchemy2 import Geometry
from database import Base
from pydantic import EmailStr, UUID4
import uuid


class Location(Base):
    __tablename__ = "location"
    
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    
    name = Column(String)
    
    id_organization = Column(UUID(as_uuid=True), 
                        ForeignKey("organization.id", 
                                  ondelete="CASCADE"))
    
    longitude = Column(Float)
    latitude = Column(Float)
    
    address = Column(String)
    
    def __init__(self, name:str, latitude:float, id_organization:UUID4, longitude:float, address:str) -> None:
        self.name = name
        self.latitude = latitude
        self.id_organization = id_organization
        self.longitude = longitude
        self.address = address