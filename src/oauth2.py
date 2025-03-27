from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from .models import Token, TokenData, User
from sqlalchemy.orm import Session
from .database import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth')

load_dotenv()
secret_key = os.getenv('JWT_SECRET_KEY_FOR_SIGNING')
algorithm = os.getenv('SIGNING_ALGORITHM')
expiration_time = os.getenv('LONG_EXPIRATION_MINUTES')

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(expiration_time))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return token

def verify_access_token(access_token: str, credentials_exception):
    try:
        payload = jwt.decode(access_token, secret_key, algorithms=[algorithm])
        id: str = payload.get('id')
        role: str = payload.get('role')
        return TokenData(id=id, role=role)
    except Exception as exception:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    tokenData: TokenData = verify_access_token(token, credentials_exception=credentials_exception)
    query = db.query(User).filter(tokenData.id == User.id)
    user = query.first()
    if not user:
        raise credentials_exception
    return user