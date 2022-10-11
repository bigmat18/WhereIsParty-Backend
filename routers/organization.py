from fastapi import APIRouter, Depends, status, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from schemas.organization import OrganizationSchema
from models import User, Organization
from database import get_db
from utils.file_manager import upload_file, delete_file, AWS_BUCKET_URL
from utils.get_current_user import get_current_user

organization_router = APIRouter(tags=['Organization'])


def get_organization(id:str, db:Session) -> Organization:
    organization = db.query(Organization).filter(Organization.id == id).first()
    if not organization: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Non esiste una organization con questo id")
    return organization



@organization_router.get(path="/organization/{id_organization}", status_code=status.HTTP_200_OK, response_model=OrganizationSchema)
def organization_retrieve(id_organization:str,
                          user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    organization = get_organization(id_organization, db)
    return organization



# @organization_router.patch(path="/organization/{id_organization}", status_code=status.HTTP_200_OK, response_model=OrganizationSchema)
# def organization_update(organization_data: OrganizationSchema,
#                         id_organization: str,
#                         user: User = Depends(get_current_user),
#                         db: Session = Depends(get_db)):
#     organization = get_organization(id_organization, db)
    
#     if organization_data.name: 
#         organization.name = organization_data.name
#     if organization_data.email: 
#         organization.email = organization_data.email
#     if organization_data.phone: 
#         organization.phone = organization_data.phone
#     if organization_data.instragram_link: 
#         organization.instagram_phone = organization_data.instragram_link
    
#     db.commit()
#     db.refresh(organization)
    
#     return organization


# @organization_router.patch(path="/organization/{id_organization}/image", status_code=status.HTTP_200_OK)
# def organizaion_image_update(id_organization: str,
#                              image: UploadFile = File(),
#                              user: User = Depends(get_current_user),
#                              db: Session = Depends(get_db)):
    
#     organization = get_organization(id_organization, db)
    
#     url = upload_file(image.file, f"/organization-{organization.id}", "organization-images")
    
#     if url and organization.image_url:
#         path = organization.image_url.replace(AWS_BUCKET_URL + "/", '')
#         try: delete_file(path)
#         except: print("Eliminazione vecchio file non riuscita")
        
#     organization.image_url = url
#     db.commit()
#     db.refresh(organization)
        
#     return {"image_url": url}