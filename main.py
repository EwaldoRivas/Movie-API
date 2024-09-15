from fastapi import  FastAPI,  HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from utils.jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from routers.user import user_router
import os
import uvicorn
import datetime
import json
from middlewares.error_handler import ErrorHandler

from routers.movie import movie_router

if __name__ =="__main__":
    uvicorn.run("main:app", host ="0.0.0.0",
                port=int(os.environ.get("PORT",8000)))

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

# Dependency para obtener la sesión de base de datos
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


class JWTBearer(HTTPBearer):
    async def __call__(self,request: Request ):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidos")



class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel):
    id: Optional [int] | None = None
    title: str = Field(min_length=5,max_length=15)
    overview : str = Field(min_length=15,max_length=50)
    year: int = Field(le=datetime.date.today().year)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5,max_length=15)

    
    model_config = {
     "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Mi Pelicula",
                    "overview": "Descripcion de la pelicula",
                    "year": 2022,
                    "rating": 9.9,
                    "category": "Acción"
                }
            ]
        }
    }
movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    }  
]

@app.get('/', tags= ["home"])
def message():
    return HTMLResponse('<h1> Jamones 2 </h1>')

@app.post('/login', tags=["auth"])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
       token: str = create_token(user.model_dump())
    return JSONResponse(status_code=200, content=token)



        
