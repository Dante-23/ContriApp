from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from pydantic import BaseModel, field_validator, root_validator
from email_validator import validate_email, EmailNotValidError
from enum import Enum
from typing import Optional

class User(Base):
    __tablename__ = 'users'  # Name of the table in the database

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    role = Column(String, default="user")

class Expenditure(Base):
    __tablename__ = 'expenditures'
    id = id = Column(String, primary_key=True)
    userid = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    
class ExpenditureContributor(Base):
    __tablename__ = 'expenditure_contributors'
    userid = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    expenditureid = Column(String, ForeignKey("expenditures.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    amount = Column(Integer, nullable=False)
    isAccepted = Column(Boolean, default=False, nullable=False)
    isPaid = Column(Boolean, default=False, nullable=False)


class Gender(str, Enum):
    male = 'male'
    female = 'female'
    Male = 'Male'
    Female = 'Female'

class UserDTO(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str
    gender: Gender
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v is None or v == "":
            raise ValueError('Name must not be null')
        elif any(char.isdigit() for char in v):
            raise ValueError('Name must contain only alphabets')
        else:
            return v.title()
        
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        try:
            email_info = validate_email(v, check_deliverability=False)
            return v
        except EmailNotValidError as e:
            raise ValueError(f'Invalid email format: {e}')
        
    @root_validator(pre=True)
    def check_passwords_match(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                raise ValueError('Passwords do not match.')
            else:
                return values
        else:
            raise ValueError('Password and confirm password are needed')       

class UserAuthDTO(BaseModel):
    email: str
    password: str
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        try:
            email_info = validate_email(v, check_deliverability=False)
            return v
        except EmailNotValidError as e:
            raise ValueError(f'Invalid email format: {e}')
        
class UserUpdateDTO(BaseModel):
    name: str
    gender: Gender
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v is None or v == "":
            raise ValueError('Name must not be null')
        elif any(char.isdigit() for char in v):
            raise ValueError('Name must contain only alphabets')
        else:
            return v.title()

class AddExpenditureDTO(BaseModel):
    userid: str
    name: str
    amount: int
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v is None or v == "":
            raise ValueError('Name must not be null')
        elif any(char.isdigit() for char in v):
            raise ValueError('Name must contain only alphabets')
        else:
            return v
        
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: int) -> int:
        if v < 0 or v > 8000000:
            raise ValueError('0 <= amount <= 8000000')
        else:
            return v

class UpdateExpenditureDTO(BaseModel):
    userid: str
    name: str
    amount: int
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v is None or v == "":
            raise ValueError('Name must not be null')
        elif any(char.isdigit() for char in v):
            raise ValueError('Name must contain only alphabets')
        else:
            return v
        
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: int) -> int:
        if v < 0 or v > 8000000:
            raise ValueError('0 <= amount <= 8000000')
        else:
            return v

class AddExpenditureContributor(BaseModel):
    userid: str
    expenditureid: str
    amount: int
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: int) -> int:
        if v < 0 or v > 8000000:
            raise ValueError('0 <= amount <= 8000000')
        else:
            return v

class Token(BaseModel):
    access_token: str

class TokenData(BaseModel):
    id: Optional[str] = None
    role: str