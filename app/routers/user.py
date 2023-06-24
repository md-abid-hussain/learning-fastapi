from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..schemas import schemas
from ..models import models
from ..utils import utils
from ..config.db import get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/', response_model=List[schemas.UserResponse])
def get_all_user(db: Session = Depends(get_db)):
    result = db.query(models.User).all()
    return result


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    is_existing = db.query(models.User).filter(
        models.User.email == user.email).first()
    if is_existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"user with email {user.email} already exists")
    # hash the password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    result = db.query(models.User).filter(models.User.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")
    return result
