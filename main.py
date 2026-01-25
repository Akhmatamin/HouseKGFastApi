from fastapi import FastAPI
from mysite.api.auth import auth_router
from mysite.api.city import city_router
from mysite.api.country import country_router
from mysite.api.property import property_router
from mysite.api.review import review_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(city_router)
app.include_router(property_router)
app.include_router(country_router)
app.include_router(review_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
