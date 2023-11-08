from enum import Enum
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


def get_dogs_from_db(kind: str):
    answer = list()
    for v in dogs_db.values():
        if v.kind == kind:
            answer.append(v)
    return answer


def create_dog_to_db(dog: Dog):
    dogs_db[len(dogs_db)] = dog


def get_dog_from_db_by_pk(pk: int):
    for k, v in dogs_db.items():
        if k == pk:
            return v
    raise HTTPException(status_code=422, detail="Validation error")


def update_dog_by_pk(pk: int, dog: Dog):
    for k, v in dogs_db.items():
        if k == pk:
            dogs_db[pk] = dog
            return dogs_db[pk]
    raise HTTPException(status_code=422, detail="Validation error")


@app.get('/', response_model=str, summary="Root")
def root():
    return "string"


@app.post('/post', response_model=Timestamp, summary="Get Post")
def get_post():
    return post_db[0]


@app.get('/dog', response_model=list, summary="Get dogs")
def get_dogs(kind: str | None = None):
    if kind:
        if kind not in DogType.__members__:
            raise HTTPException(status_code=422, detail="Validation error")
        return get_dogs_from_db(kind)
    else:
        return [dog for dog in dogs_db.values()]


@app.post('/dog', response_model=Dog, summary="Create dog")
def create_dog(dog: Dog):
    create_dog_to_db(dog)
    return dog


@app.get('/dog/{pk}', response_model=Dog, summary="Get dog by pk")
def get_dog_by_pk(pk: int):
    dog = get_dog_from_db_by_pk(pk)
    return dog


@app.patch('/dog/{pk}', response_model=Dog, summary="Update dog")
def update_dog(pk: int, dog: Dog):
    updated_dog = update_dog_by_pk(pk, dog)
    return updated_dog

uvicorn.run(app)