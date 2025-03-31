from fastapi import status, Depends, APIRouter, HTTPException
from ..models import User, Expenditure, ExpenditureContributor, AddExpenditureContributor
from ..utils import generate_uuid_string
from ..database import get_db
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user

router = APIRouter(
    prefix='/expenditurecontributors',
    tags=['Expenditure contributors']
)

@router.get("/{userid}")
def get_all_pending_contributions(userid: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)): 
    if userid != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token and userid mismatch")
    contributions = db.query(ExpenditureContributor).filter(ExpenditureContributor.userid == userid).all()
    return {"Contributions": contributions}

@router.post('/', status_code = status.HTTP_201_CREATED)
def add_pending_contribution(contributor: AddExpenditureContributor, db: Session = Depends(get_db), 
             user: User = Depends(get_current_user)):
    contribution: ExpenditureContributor = ExpenditureContributor(userid=contributor.userid,
                                                                  expenditureid=contributor.expenditureid,
                                                                  amount=contributor.amount)
    try:
        db.add(contribution)
        db.commit()
        db.refresh(contribution)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Some error occurred while adding contribution")
    return {"New contribution": contribution}