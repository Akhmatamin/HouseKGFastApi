from fastapi import APIRouter, Depends, HTTPException
from mysite.database.models import Country
from mysite.database.schema import CountrySchema,CountryCreate,CountryRead
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session

country_router = APIRouter(prefix="/country", tags=["Country"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@country_router.get("/", response_model=CountryRead)
async def get_country(db: Session = Depends(get_db)):
    return db.query(Country).all()

@country_router.post("/create", response_model=CountryRead)
async def create_country(country_data: CountryCreate, db: Session = Depends(get_db)):
    country_db = CountryCreate(**country_data.dict())
    db.add(country_db)
    db.commit()
    db.refresh(country_db)
    return country_db

@country_router.put("/{id}", response_model=CountryRead)
async def update_country(country_id:int,country_data: CountrySchema, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id==country_id).first()
    if country_db is None:
        raise HTTPException(status_code=404, detail="Country not found")
    for key, value in country_data.dict().items():
        setattr(country_db, key, value)
    db.commit()
    db.refresh(country_db)
    return country_db

@country_router.delete("/delete", response_model=dict)
async def delete_country(country_id:int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id==country_id).first()
    if country_db is None:
        raise HTTPException(status_code=404, detail="Country not found")
    db.delete(country_db)
    db.commit()
    return {'message': 'Country deleted'}

