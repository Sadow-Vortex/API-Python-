#import uuid
# from enum import verify
# from uuid import uuid4

from fastapi import FastAPI,HTTPException,Depends,status,UploadFile,File
from pydantic import BaseModel
from typing import Annotated, Optional
from sqlalchemy.orm import Session
# from sqlalchemy.orm.sync import update
# from sqlalchemy.testing.suite.test_reflection import users
from models import models
from config.db import engine,sessionLocal
from io import BytesIO
from fastapi.responses import StreamingResponse

app = FastAPI()
models.base.metadata.create_all(bind=engine)

class PokeIndex(BaseModel):
    rank : Optional[int] = None
    name : Optional[str] = None
    type : Optional[str] = None
    strength : Optional[int] = None
    speed : Optional[int] = None
    health : Optional[int] = None
    defence : Optional[int] = None
    Power_against_increase : Optional[str] = None
    description : Optional[str] = None
    Power_against_decrease : Optional[str] = None

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]

@app.get("/h")
async def get(user_id : int, db: Session = Depends(get_db)):
    user_n = db.query(models.Pokemon).filter(models.Pokemon.id==user_id)

    if not user_n:
        raise HTTPException(status_code = 404 , detail = "User doesn't exist")
    return user_n

@app.post("/home/post")
async def stdent_post(post_id:PokeIndex, db: db_dependency):
    users_post = models.Pokemon(**post_id.dict())
    db.add(users_post)
    db.commit()
    db.refresh(users_post)
    return users_post
@app.post("/upload-pokemon/")
async def upload_pokemon(pokemon: PokeIndex,db: db_dependency ,image: UploadFile = File(...)):
    # Check if the uploaded file is an image
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Read image data as binary
    image_data = await image.read()

    # Create a new Pokémon entry
    db_pokemon = models.Pokemon(**pokemon.model_dump(), image=image_data)
    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)

    return {"id": db_pokemon.id, "name": db_pokemon.name}

@app.post("/home/post",status_code=status.HTTP_201_CREATED)
async def creat(posts: PokeIndex, db: db_dependency):
    # if not image.content_type.startswith("image/"):
    #     raise HTTPException(status_code=400, detail="File must be an image")

    # image_data = await image.read()

    db_pokemon = models.Pokemon(**posts.dict())

    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon

# @app.post("/home/post/gpt", status_code=status.HTTP_201_CREATED)
# async def creat(posts: PokeIndex, db: db_dependency, image: UploadFile = File(...)):
#     # Validate that the uploaded file is an image
#     if not image.content_type.startswith("image/"):
#         raise HTTPException(status_code=400, detail="File must be an image")
#
#     # Read the image data as binary
#     image_data = await image.read()
#
#     # Corrected: Convert Pydantic model to dictionary using .dict()
#     db_pokemon = models.Pokemon(**posts.dict(), image=image_data)  # <-- Fixed line
#
#     # Add the new Pokemon entry to the database
#     db.add(db_pokemon)
#     db.commit()
#     db.refresh(db_pokemon)
#
#     return db_pokemon

#
#
@app.get("/users/{poke_id}/post", status_code=status.HTTP_200_OK)
async def read_user(Poke_id: int, db: Session = Depends(get_db)):
    print(f"Poke Index session active: {db}")
    Poke_n = db.query(models.Pokemon).filter(models.Pokemon.id == Poke_id).first()

    if not Poke_n:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return Poke_n
#
# # @app.get("/users/{poke_id}/post/image")
# # async def pokemon_image(poke_id: int,db : db_dependency):
# #     db_pokemon = db.query(models.Pokemon).filter(models.Pokemon.id==poke_id).first()
# #     if not db_pokemon or not db_pokemon.image:
# #         raise HTTPException(status_code=404, detail="Image not found")
# #
# #     return StreamingResponse(BytesIO(db_pokemon.image),media_type="image/jpeg")
#
#
@app.put("/posts/{post_id}",status_code=status.HTTP_200_OK,response_model=PokeIndex)
async def update_user(poke_id: int, post_update: PokeIndex, db: db_dependency):

    db_post = db.query(models.Pokemon).filter(models.Pokemon.id == poke_id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail={"Pokemon data not avilable"})

    update_data = post_update.model_dump()
    for key, value in update_data.items():
        setattr(db_post,key,value)

    # if image:
    #     if not image.content_type.startswith("image/"):
    #         raise HTTPException(status_code=400, detail="Pokemon Image not found")
    #     db_post.image = await image.read()

    db.commit()
    db.refresh(db_post)
    return db_post
#
#
@app.delete("/home/user/{poke_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(poke_id: int, db: db_dependency):
    db_user = db.query(models.Pokemon).filter(models.Pokemon.id == poke_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Pokemon not found")

    db.delete(db_user)
    db.commit()
    return ("Pokemon release sucessfully")
#
