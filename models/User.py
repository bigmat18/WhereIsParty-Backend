from sqlalchemy.sql.expression import text
from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base
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
    
    password = Column(String(64))
    
    def __init__(self, password, email, first_name, last_name):
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name