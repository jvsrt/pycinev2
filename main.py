from fastapi import FastAPI, Depends, status, Request, Response, APIRouter, HTTPException
from fastapi.middleware.cors import (
     CORSMiddleware
)
from pydantic import BaseModel
# Precisamos importar MovieUtils e Genre:
from tmdb.models import Genre
from tmdb.api_utils import (
    RequestApi, MovieUtils, ArtistaUtils
)

import schemas, models
from database import engine
from sqlalchemy.orm import Session

import database


app = FastAPI()
models.Base.metadata.create_all(engine)


origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    
)


class User(BaseModel):
    name: str
    email: str
    password: str

@app.post('/user', status_code=status.HTTP_201_CREATED, tags=['users'])
def create_user(request: schemas.UserModel, db: Session = Depends(database.get_db)):
    
    new_user = models.User(name=request.name, email=request.email, password=request.password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/user', tags=['users'])
def all(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


@app.get('/user/{id}',status_code=200 ,tags=['users'])
def get_user_by_id(id, response: Response, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"User with the id {id} isnt available")
    return user

@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['users'])
def delete_user(id, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['users'])
def update_user(id, request: User, db: Session = Depends(database.get_db)):

    print(request)
    print(id, 'id teste')
    user = db.query(models.User).filter(models.User.id == id)
    
    if not user.first():
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with id {id} not found")

    user.update({'name':request.name, 'email':request.email, 'password':request.password})

    
    db.commit()
    return 'updated'


# fornecido um id, retorno o 
# json do filme
# /movie/1
@app.get("/movie/{id}")
async def get_movie(id: int):
    import json
    # lista de dictionary
    data = json.load(open('filmes.json'))
    for filme in data:
        if filme['id'] == id:
            return filme
    return {}

# TODO: get_genres

@app.get("/movies_json")
async def get_movies_json():
    import json
    data = json.load(open('filmes.json'))
    return data

@app.get("/movies")
async def get_movies():
    # chamar a classe MovieUtils para consultar TMDB
    movies = MovieUtils.get_movies(Genre.Scifi.value)
    return movies

@app.get("/artista/id/{id}")
async def get_artista(id):
    artista = RequestApi.get_artista(id)
    return artista

# Objetivo: Implementar o endpoint para 
# encontrar artistas pelo nome fornecido como 
# parametro na url.
# - Retorna uma lista de artistas.
# - Exemplo de endpoint na nossa API:
# /artista/name/arnold

@app.get("/artista/name/{name}")
async def get_artista_by_name(name):
    artista = ArtistaUtils.get_artistas(name)
    
    return artista[0]


@app.get("/find/{title}/{genre}")
async def find(title: str, genre):
    import json
    data = json.load(open('filmes.json'))
    encontrou = []
    for filme in data:
        # in - contains (ou contem um substring)
        if title.lower() in filme['title'].lower():
            # append - adiciona na lista
            encontrou.append(filme)
    return encontrou

@app.get("/")  # HTTP GET
async def home():
    return {"msg": "Hello"}

# rodar o fastapi:
# uvicorn main:app --reload

# pip install -r requirements.txt
# source env/
# pip install fastapi uvicorn
