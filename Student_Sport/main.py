from typing import List,Optional, Any

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

import models
from db import base, sessionlocal, engine
from models import StudentSportAssociation

app = FastAPI()
models.base.metadata.create_all(bind=base)
models.base.metadata.create_all(bind=engine)

class StudentSportLink(BaseModel):
    student_id: int
    sport_ids: List[int]
    created_by: str
    updated_by: Optional[str] = None

    class Config:
        orm_mode = True
        from_attribute = True

class Response(BaseModel):
    status_code: int
    status: str
    data: Optional[Any] = None
    message: str

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.get("home/",response_model=Response)
async def student_sports(db: Session = Depends(get_db)):
    try:
        all_data = db.query(models.StudentSportAssociation).all()
        all_data_dict = [StudentSportLink.from_orm(StudentSportAssociation) for StudentSportAssociation in all_data]
        if not all_data:
            return Response(
                status_code=200,
                status="Success",

                data=[],
                message="Table is empty"
            )
        return Response(
            status_code=200,
            status="Success",
            data=all_data_dict,
            message="Table is empty"
        )
    except Exception as e:
        return Response(
            status_code=404,
            status="failed",
            data=str(e),
            message="problem occured"
        )