from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class RoleChoices(str, Enum):
    seller = "seller"
    buyer = "buyer"
    admin = "admin"


class PropertyType(str, Enum):
    apartment = "apartment"
    house = "house"
    parking = "parking"
    commercial = "commercial"
    office = "office"
    area = "area"



class UserSchema(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    role: RoleChoices = RoleChoices.buyer


class UserCreate(UserSchema):
    password: str

class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserDetail(UserSchema):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserRead(BaseModel):
    id: int
    username: str



class CountrySchema(BaseModel):
    name: str


class CountryCreate(CountrySchema):
    pass


class CountryRead(CountrySchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CitySchema(BaseModel):
    name: str
    country_id: int


class CityCreate(CitySchema):
    pass


class CityRead(CitySchema):
    id: int
    country: CountryRead

    model_config = ConfigDict(from_attributes=True)



class PropertySchema(BaseModel):
    title: str
    type: PropertyType
    district: str
    address: str
    price: float
    area: float

    rooms: Optional[int] = None
    floor: Optional[int] = None
    total_floors: Optional[int] = None

    condition: str
    security: str
    documents: str
    rassrochka: bool = False
    description: str
    rating: float = Field(ge=0, le=5)


class PropertyCreate(PropertySchema):
    city_id: int


class PropertyList(BaseModel):
    title: str
    type: PropertyType
    address: str
    price: float
    area: float


class PropertyImageCreate(BaseModel):
    property_id: int
    image: str


class PropertyImageRead(BaseModel):
    id: int
    image: str

    model_config = ConfigDict(from_attributes=True)



class ReviewBase(BaseModel):
    comment: Optional[str] = None
    rating: int = Field(ge=1, le=5)


class ReviewCreate(ReviewBase):
    property_id: int


class ReviewRead(ReviewBase):
    id: int
    date_added: datetime
    user: UserRead

    model_config = ConfigDict(from_attributes=True)
