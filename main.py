from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, SessionLocal, engine

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from models import User, Organization

from routers.auth import auth_router
from routers.organization import organization_router
from routers.location import location_router
from routers.event import event_router


Base.metadata.create_all(bind=engine)
app = FastAPI()
db = SessionLocal()


# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
    authjwt_secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    authjwt_denylist_enabled: bool = True


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()


# get id user and set it logged out from rest api
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    user_id = decrypted_token['sub']
    user = db.query(User).filter(User.id == user_id).first()
    return user.access_revoked


# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(organization_router)
app.include_router(location_router)
app.include_router(event_router)


# Create admin user
user = db.query(User).filter(User.email == "admin@admin.com").first()
if not user:
    user = User("admin123456", "admin@admin.com", "admin", "admin")
    db.add(user)
    db.commit()
    
# Create default organization
if not db.query(Organization).filter(Organization.email == "test@test.com").first():
    organization = Organization("test", "test@test.com", user.id)
    db.add(organization)
    db.commit()
    db.refresh(organization)
    print(organization.id)