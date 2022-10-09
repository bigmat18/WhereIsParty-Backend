from pydantic import UUID4, BaseModel, EmailStr
from typing import Union

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    

class AuthenticationSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class UserSchema(BaseModel):
    id: UUID4
    email: EmailStr
    first_name: str
    last_name: str
    image_url: Union[str, None]
    
    class Config:
        orm_mode = True