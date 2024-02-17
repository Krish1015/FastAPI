from fastapi import APIRouter, HTTPException, Response, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, models, utils, connect_database, Oauth2
from sqlalchemy.orm import Session

router = APIRouter(tags= ["Authentication"])

@router.post("/login")
def login(user_credn:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(connect_database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credn.username).first()
    #user = db.query(models.User).filter(models.User.email == user_credn.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")
    if not utils.verify(user_credn.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password")
    access_token = Oauth2.create_access_token(data = {'user_id': user.id})
    
    return {"AccessToken": access_token, "TokenType":"Bearer"}



