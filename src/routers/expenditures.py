from fastapi import Response, status, Depends, APIRouter, HTTPException
from ..models import User, Expenditure, AddExpenditureDTO, UpdateExpenditureDTO
from ..utils import generate_uuid_string
from ..database import get_db
from sqlalchemy.orm import Session
from ..oauth2 import create_jwt_token, get_current_user

router = APIRouter(
    prefix='/expenditures',
    tags=['Expenditures']
)

'''
* Add two users - Rock and Shock
* Authenticate Rock and obtain auth token
* Add two expenditures (Food, 500) and (Travel, 100) for Rock
* Add three expenditures (Party, 800), (Snacks, 100) and (Tickets, 1500)  for Shock
* Fetch expenditures of Rock
* Fetch expenditures of Shock
* Update Rock expenditure of (Food, 500) to (Food, 600)
* Fetch expenditures of Rock
* Fetch expenditures of Shock
* Delete Shock expenditure of (Tickets, 1500)
* Fetch expenditures of Rock
* Fetch expenditures of Shock
* Delete Rock
* Fetch expenditures of Rock
* Fetch expenditures of Shock
* Delete Shock
* Fetch expenditures of Rock
* Fetch expenditures of Shock
'''

@router.get("/{userid}")
def get_all_expenditures(userid: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)): 
    if userid != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token and userid mismatch")
    expenditures = db.query(Expenditure).filter(Expenditure.userid == userid).all()
    print(db.query(Expenditure).filter(Expenditure.userid == userid))
    return {"Expenditures": expenditures}

@router.post('/', status_code = status.HTTP_201_CREATED)
def add_expenditure(expenditureFromRequest: AddExpenditureDTO, db: Session = Depends(get_db), 
             user: User = Depends(get_current_user)):
    if expenditureFromRequest.userid != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token and userid mismatch")
    expenditure: Expenditure = Expenditure(id=generate_uuid_string(), 
                                           userid=expenditureFromRequest.userid, 
                                           name=expenditureFromRequest.name,
                                           amount=expenditureFromRequest.amount)
    try:
        db.add(expenditure)
        db.commit()
        db.refresh(expenditure)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Some error occurred while adding expenditure")
    return {"New expenditure": expenditure}

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_expenditure(id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    expenditureQuery = db.query(Expenditure).filter(id == Expenditure.id)
    if expenditureQuery.first() == None or expenditureQuery.first().userid != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token and userid mismatch")
    expenditureQuery.delete(synchronize_session=False)
    db.commit()
    return

@router.put('/{id}', status_code = status.HTTP_200_OK)
def update_expenditure(id: str, updateExpenditureRequest: UpdateExpenditureDTO,
                        db: Session = Depends(get_db), 
                        userFromToken: User = Depends(get_current_user)):
    if userFromToken.id != updateExpenditureRequest.userid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token and userid mismatch")
    query = db.query(Expenditure).filter(id == Expenditure.id)
    expenditure: Expenditure = query.first()
    if not expenditure:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Expenditure with given id not found")
    updatedExpenditure = Expenditure(id=expenditure.id, userid=expenditure.userid,
                                     name=updateExpenditureRequest.name,
                                     amount=updateExpenditureRequest.amount,
                                     created_at=expenditure.created_at)
    query.update({'id': expenditure.id, 'name': updateExpenditureRequest.name, 
                  'amount': updateExpenditureRequest.amount,
                  'created_at': expenditure.created_at}, synchronize_session=False)
    db.commit()
    return {"User": updatedExpenditure}