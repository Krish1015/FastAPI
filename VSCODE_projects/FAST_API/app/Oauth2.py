from jose import JWTError, jwt
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from . import schemas, connect_database, models
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# Secret Key
# Algorithm
# Expiration Time   

SECRET_KEY = "f0fif29040f09jfjw0jd09j34jf09jjasaczmcnnf33icnnxasanm"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 30

def create_access_token(data: dict):
    df = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    df.update({'exp':exp})
    return jwt.encode(df, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        id: str = payload.get('user_id')
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        print("JWT Error")
        raise credentials_exception
    print(token_data)
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme),db: Session =  Depends(connect_database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == int(token.id)).first()
    print(user)
    return user





