from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

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