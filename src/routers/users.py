from fastapi import Response, status, Depends, APIRouter, HTTPException
from ..models import User, UserDTO, UserAuthDTO, UserUpdateDTO
from ..utils import generate_uuid_string, hash_password, verify_password
from ..database import get_db
from sqlalchemy.orm import Session
from ..oauth2 import create_jwt_token, get_current_user

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get("/")
def get_all_users(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user is None or user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin access required")
    users = db.query(User).all()
    return {"Users": users}

@router.post('/', status_code = status.HTTP_201_CREATED)
def add_user(user: UserDTO, response: Response, db: Session = Depends(get_db)):
    db_user = User(id=generate_uuid_string(), name=user.name, email=user.email,
                   password=hash_password(user.password), gender=user.gender, role='user')
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as exception:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": "There is some error in the input provided"}
    return {"New user": db_user}

@router.post('/auth', status_code = status.HTTP_200_OK)
def authenticate_user(user: UserAuthDTO, response: Response, db: Session = Depends(get_db)):
    users = db.query(User).filter(user.email == User.email).all()
    if len(users) > 1:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Status": "More than one email exist"}
    elif len(users) == 0:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Status": "User not found"}
    elif users is not None:
        db_user = users[0]
        hashed_password = getattr(db_user, 'password')
        if verify_password(plain_password=user.password, hashed_password=hashed_password):
            userRole = "user"
            tokenData = {
                "id": getattr(db_user, 'id'),
                "role": userRole
            }
            access_token = create_jwt_token(data=tokenData)
            return {"Status": "Authentication successfull", "Token": access_token, "Id": getattr(db_user, 'id'), "Role": userRole}
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"Status": "Authentication failed"}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Status": "User not found"}

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(id: str, response: Response, db: Session = Depends(get_db), userFromToken: User = Depends(get_current_user)):
    if userFromToken.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token and id mismatch")
    users = db.query(User).filter(id == User.id)
    if users.first() == None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"Status": "More than one such user exist"}
    users.delete(synchronize_session=False)
    db.commit()
    return

@router.get('/{id}', status_code = status.HTTP_200_OK)
def get_user(id: str, response: Response, db: Session = Depends(get_db), userFromToken: User = Depends(get_current_user)):
    if userFromToken.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token and id mismatch")
    user = db.query(User).filter(id == User.id).all()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"User": None}
    return {"User": user}

@router.put('/{id}', status_code = status.HTTP_200_OK)
def update_user(id: str, updateUserRequest: UserUpdateDTO, response: Response, db: Session = Depends(get_db), 
                userFromToken: User = Depends(get_current_user)):
    if userFromToken.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token and id mismatch")
    user_query = db.query(User).filter(id == User.id)
    user = user_query.first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"User": None}
    updated_user = User(id=user.id, name=updateUserRequest.name, gender=updateUserRequest.gender, 
                        email=user.email, password=user.password)
    user_query.update({'id': user.id, 'name': updateUserRequest.name, 'gender': updateUserRequest.gender, 
                       'email': user.email, 'password': user.password}, synchronize_session=False)
    db.commit()
    return {"User": updated_user}