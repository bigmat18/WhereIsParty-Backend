from fastapi import APIRouter, Depends, status, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from schemas.organization import ReferralLinkSchema
from models import User, ReferralLink, ReferralLinkUser
from database import get_db
from utils.file_manager import delete_file, upload_file, AWS_BUCKET_URL
from utils.get_current_user import get_current_user
from .organization import get_organization


referral_link_router = APIRouter(tags=["ReferralLink"])


def get_referral_link(id:str, db:Session) -> ReferralLink:
    referral_link = db.query(ReferralLink).filter(ReferralLink.id == id).first()
    if not referral_link: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Non esiste una referral link con questo id")
    return referral_link


@referral_link_router.post(path="/organization/{id_organization}/referrals", status_code=status.HTTP_201_CREATED, response_model=ReferralLinkSchema)
def referral_link_create(id_organization:str,
                         referral_link_data: ReferralLinkSchema,
                         user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    organization = get_organization(id_organization, db)
    
    referral_link = ReferralLink(referral_link_data.name, organization.id)
    
    db.add(referral_link)
    db.commit()
    db.refresh(referral_link)
    
    for user_id in referral_link_data.users:
        if db.query(User).filter(User.id == user_id).first():
            user = ReferralLinkUser(user_id, referral_link.id)
            db.add(user)
    
    db.commit()
            
    return referral_link
