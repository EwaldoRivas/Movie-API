from fastapi import APIRouter
from fastapi import Depends,  Path, Query
from fastapi.responses import  JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
import datetime
import json
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie




movie_router = APIRouter()


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

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200,  dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]: 
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})  # Corregido para devolver la respuesta
    return JSONResponse(status_code=200, content=jsonable_encoder(result))  # Corregido 'ontent' a 'content'


@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category:str = Query(min_length=5,max_length=15)) -> List[Movie]:
    db= Session()
    result = MovieService(db).get_movies_by_category(category)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**json.loads(movie.model_dump_json()))
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201,content={"message": " se ha registrado la pelicula"})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie:Movie)-> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    MovieService(db).update_movie(id, movie)
    db.commit()

    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:
    db = Session()
    result = MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    MovieService(db).delete_movie(id)


    return JSONResponse(status_code=200, content={"message": " se ha eliminado la pelicula"})