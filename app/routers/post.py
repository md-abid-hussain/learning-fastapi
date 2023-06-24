from typing import List, Optional
from fastapi import Depends, status, Response, HTTPException, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from ..models import models
from ..config.db import get_db
from ..schemas import schemas
from ..utils import oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[schemas.PostOut])
def get_all_post(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    return results


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # print(**post.dict()) **post.dict() similar to spread operator in js
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    post = results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not found")
    return post


@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    result = delete_query.first()
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"post with id {id} not found in db")

    if result.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized")

    result = delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    result_query = db.query(models.Post).filter(models.Post.id == id)
    result = result_query.first()
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"post with id {id} not found in db")

    if result.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='not authorized')
    # update require a dictionary
    result_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return result_query.first()
