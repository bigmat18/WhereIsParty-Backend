from sqlalchemy.sql.expression import text
from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base
from werkzeug.security import (generate_password_hash, 
                               check_password_hash)
import uuid


class User(Base):
    __tablename__ = "user"
    
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4)
    
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    
    date_joined = Column(TIMESTAMP(timezone=True),
                         server_default=text('now()'))
    last_login = Column(TIMESTAMP(timezone=True),
                        nullable=True)
    
    image_url = Column(String, nullable=True)
    
    password = Column(String(64))
    
    access_revoked = Column(BOOLEAN, default=False)
    
    def __init__(self, password:str, email:str, first_name:str, last_name:str):
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(pwhash=self.password,
                                   password=password)