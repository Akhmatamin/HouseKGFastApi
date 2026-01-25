from fastapi import APIRouter, Depends, HTTPException
from mysite.database.models import Review
from mysite.database.schema import *
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

review_router = APIRouter(prefix="/review", tags=["review"])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@review_router.get('/',response_model=List[ReviewRead])
async def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()

@review_router.post('/',response_model=ReviewRead)
async def create_review(data: ReviewCreate, db: Session = Depends(get_db)):
    review_db = Review(**data.dict())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db

@review_router.delete('/{review_id}',response_model=dict)
async def delete_review(review_id:int,db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if review_db is None:
        raise HTTPException(status_code=404, detail="Review Not Found")
    db.delete(review_db)
    db.commit()
    return {'message': 'Review Deleted'}

