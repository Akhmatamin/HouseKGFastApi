from datetime import date,datetime
from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Enum, Text, ForeignKey, Boolean, Date, DateTime, DECIMAL
from typing import Optional, List
from enum import Enum as PyEnum

class RoleChoices(str, PyEnum):
    seller = "seller"
    buyer = "buyer"
    admin = "admin"

class PropertyType(str, PyEnum):
    apartment = "apartment"
    house = "house"
    parking = "parking"
    commercial = "commercial"
    office = "office"
    area = "area"



class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)
    first_name: Mapped[str | None ] = mapped_column(String(150),nullable=True)
    last_name: Mapped[str] = mapped_column(String(150),nullable=True)
    password: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.buyer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    properties = relationship("Property", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    user_tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='token_user',
                                                             cascade='all, delete-orphan')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String)

    user_id:Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
    token_user:Mapped[UserProfile] = relationship('UserProfile', back_populates='user_tokens')
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    cities = relationship("City", back_populates="country")

    def __str__(self):
        return self.name


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))

    country = relationship("Country", back_populates="cities")
    properties = relationship("Property", back_populates="city")

    def __str__(self):
        return self.name


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))

    title: Mapped[str] = mapped_column(String(50))
    type: Mapped[PropertyType] = mapped_column(Enum(PropertyType))
    district: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    area: Mapped[float] = mapped_column(DECIMAL(10, 2))

    rooms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    floor: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_floors: Mapped[int | None] = mapped_column(Integer, nullable=True)

    condition: Mapped[str] = mapped_column(String(200))
    security: Mapped[str] = mapped_column(String(50))
    documents: Mapped[str] = mapped_column(String(200))
    rassrochka: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[str] = mapped_column(Text)
    rating: Mapped[float] = mapped_column(DECIMAL(3, 1))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship("UserProfile", back_populates="properties")
    city = relationship("City", back_populates="properties")
    images = relationship("PropertyImage", back_populates="property", cascade="all, delete")
    reviews = relationship("Review", back_populates="property", cascade="all, delete")

    def __str__(self):
        return self.title


class PropertyImage(Base):
    __tablename__ = "property_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    image: Mapped[str] = mapped_column(String(255))

    property = relationship("Property", back_populates="images")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"))
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))

    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    rating: Mapped[int] = mapped_column(Integer)
    date_added: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("UserProfile", back_populates="reviews")
    property = relationship("Property", back_populates="reviews")

    def __str__(self):
        return self.property.title

