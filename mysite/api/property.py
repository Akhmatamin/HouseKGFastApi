
from fastapi import APIRouter, Depends, HTTPException
from mysite.database.models import Property, PropertyImage
from mysite.database.schema import *
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

property_router = APIRouter(prefix="/property", tags=["property"])
property_image_router = APIRouter(prefix='/images', tags=["PropertyImages"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@property_router.get("/", response_model=List[PropertyList])
async def get_property(db: Session = Depends(get_db)):
    return db.query(Property).all()

@property_router.get("/{property_id}", response_model=PropertySchema)
async def get_property_detail(property_id: int, db: Session = Depends(get_db)):
    property_db = db.query(Property).filter(Property.id == property_id).first()
    if property_db is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_db

@property_router.post("/", response_model=PropertySchema)
async def create_property(property_data:PropertyCreate, db: Session = Depends(get_db)):
    property_db = Property(**property_data.dict())
    db.add(property_db)
    db.commit()
    db.refresh(property_db)
    return property_db

@property_router.put("/{property_id}", response_model=PropertySchema)
async def property_update(property_id:int,property_data:PropertyCreate, db: Session = Depends(get_db)):
    property_db = db.query(Property).filter(Property.id == property_id).first()
    if property_db is None:
        raise HTTPException(status_code=400, detail="Property not found")
    for key, value in property_data.items():
        setattr(property_db, key, value)
    db.commit()
    db.refresh(property_db)
    return {'message': 'Property updated successfully'}


@property_router.delete("/{property_id}",response_model=dict)
async def delete_property(property_id:int, db:Session= Depends(get_db)):
    property_db = db.query(Property).filter(Property.id == property_id).first()
    if property_db is None:
        raise HTTPException(status_code=400, detail="Property not found")
    db.delete(property_db)
    db.commit()
    return {'message':'Property deleted successfully'}



@property_image_router.get("/",response_model=List[PropertyImageRead])
async def get_property(db: Session = Depends(get_db)):
    return db.query(PropertyImage).all()

@property_image_router.get("/{image_id}",response_model=PropertyImageRead)
async def detail_property(image_id:int, db:Session= Depends(get_db)):
    property_db = db.query(PropertyImage).filter(PropertyImage.id == image_id).first()
    if property_db is None:
        raise HTTPException(status_code=400, detail="Property not found")
    return property_db

@property_image_router.post("/",response_model=dict)
async def update_image(image_id:int, image_data:PropertyImageCreate, db:Session= Depends(get_db)):
    image_db = PropertyImage(**image_data.dict())
    db.add(image_db)
    db.commit()
    db.refresh(image_db)
    return {'message':'Images added successfully'}

@property_image_router.put("/{image_id}",response_model=dict)
async def update_image(image_id:int, image_data:PropertyImageCreate, db:Session= Depends(get_db)):
    image_db = db.query(PropertyImage).filter(PropertyImage.id == image_id).first()
    if image_db is None:
        raise HTTPException(status_code=400, detail="Image not found")
    for key,value in image_data.items():
        setattr(image_db, key, value)
    db.commit()
    db.refresh(image_db)
    return {'message': 'Images updated successfully'}

@property_image_router.delete("/{image_id}",response_model=dict)
async def delete_image(image_id:int, db:Session= Depends(get_db)):
    image_db = db.query(PropertyImage).filter(PropertyImage.id == image_id).first()
    if image_db is None:
        raise HTTPException(status_code=400, detail="Image not found")
    db.delete(image_db)
    db.commit()
    return {'message': 'Images deleted successfully'}