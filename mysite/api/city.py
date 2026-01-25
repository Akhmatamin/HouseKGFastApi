from fastapi import APIRouter, Depends, HTTPException
from mysite.database.models import City
from mysite.database.schema import CitySchema,CityCreate,CityRead
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


city_router = APIRouter(prefix="/cities", tags=["Cities"])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@city_router.get("/", response_model=CityRead)
async def get_cities(db: Session = Depends(get_db)):
    cities = db.query(City).all()
    return cities

@city_router.post('/',response_model=CitySchema)
async def create_city(city:CityCreate, db: Session = Depends(get_db)):
    city_db = City(**city.dict())
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db


@city_router.put("/{city_id}",response_model=dict)
async def update_city(city_id:int,city_data:CityCreate, db:Session=Depends(get_db)):
    city_db = db.query(City).filter(City.id==city_id).first()
    if city_db is None:
        raise HTTPException(status_code=400, detail="City not found")
    for key,value in city_data.dict().items():
        setattr(city_db,key,value)
    db.commit()
    db.refresh(city_db)
    return {'message':'City updated successfully!'}

@city_router.delete("/{city_id}",response_model=dict)
async def delete_city(city_id:int,db:Session=Depends(get_db)):
    city_db = db.query(City).filter(City.id==city_id).first()
    if city_db is None:
        raise HTTPException(status_code=400, detail="City not found")
    db.delete(city_db)
    db.commit()
    return {'message':'City deleted successfully!'}

