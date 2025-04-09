from typing import Optional, Any
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from db import engine, sessionLocal

student_router = APIRouter()
app = FastAPI()
models.base.metadata.create_all(bind=engine)

class Address(BaseModel):
    At: str
    Post: str
    Block: str
    District: str
    Pin_code: str

class StudentData(BaseModel):
    student_Name: Optional[str] = None
    student_Father_Name: Optional[str] = None
    student_Age: Optional[int] = None
    student_School_Name: Optional[str] = None
    student_Class: Optional[int] = None
    student_Village: Address

    class Config:
        from_attributes = True
        orm_mode = True

class ResponseModel(BaseModel):
    status_code: int
    status: str
    Student_Id: Optional[Any] = None
    data: Optional[Any] = None
    message: str

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Corrected usage of Depends
@student_router.get("student/endpoint")
@app.get("/home/StudentData", status_code=200, response_model=ResponseModel)
async def student_data(db: Session = Depends(get_db)):
    try:
        all_data = db.query(models.Student).all()
        student_dict = [StudentData.from_orm(student) for student in all_data]
        if not all_data:
            return ResponseModel(
                status_code=200,
                status="Success",
                data=[],
                message="Student Table is empty."
            )
        return ResponseModel(
            status_code=200,
            status="Success",
            data=student_dict,
            message="All Student Data."
        )

    except Exception as e:
        return ResponseModel(
            status_code=500,
            status="Failed",
            data=str(e),
            message="Internal Server Error"
        )

@app.get("/home/StudentData/StudentDataById/{user_id}", response_model=ResponseModel)
async def student_data_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        student_n = db.query(models.Student).filter(models.Student.student_id == user_id).first()
        if not student_n:
            raise HTTPException(status_code=404, detail="Student data doesn't exist")
        student_data = StudentData.from_orm(student_n)
        return ResponseModel(
            status_code=200,
            status="Success",
            Student_Id=user_id,
            data=student_data,
            message="Student data found successfully."
        )
    except Exception as e:
        return ResponseModel(
            status_code=404,
            status="Failed",
            Student_Id=user_id,
            data=str(e),
            message="Student data not found."
        )

@app.post("/home")
async def student_register(post_id: StudentData, db: Session = Depends(get_db)):
    try:
        user_post = models.Student(**post_id.model_dump())
        db.add(user_post)
        db.commit()
        db.refresh(user_post)
        id = user_post.student_id
        user_data = StudentData.from_orm(user_post)
        return ResponseModel(
            status_code=200,
            status="Success",
            Student_Id = id,
            data=user_data,
            message="Student data inserted successfully."
        )
    except Exception as e:
        return ResponseModel(
            status_code=404,
            status="Failed",
            Student_Id=id,
            data=str(e),
            message="Student data is not inserted."
        )

@app.put("/home/StudentData/UpdateData/{user_id}", status_code=status.HTTP_200_OK, response_model=StudentData)
async def update_student_data(user_id: int, post_update: StudentData, db: Session = Depends(get_db)):
    try:
        student_n = db.query(models.Student).filter(models.Student.student_id == user_id).first()

        if not student_n:
            raise HTTPException(status_code=404, detail="Student data doesn't exist.")

        update_data = post_update.model_dump()
        for key, value in update_data.items():
            setattr(student_n, key, value)

        db.commit()
        db.refresh(student_n)
        updated_n = StudentData.from_orm(update_data)
        return ResponseModel(
            status_code=200,
            status="Success",
            Student_Id=user_id,
            data=updated_n,
            message="Student data updated successfully."
        )
    except Exception as e:
        return ResponseModel(
            status_code=404,
            status="Failed",
            Student_Id=user_id,
            data=str(e),
            message="Student data is not updated."
        )

@app.delete("/home/StudentData/student/{user_id}")
async def delete_data(user_id: int, db: Session = Depends(get_db)):
    try:
        student_n = db.query(models.Student).filter(models.Student.student_id == user_id).first()
        if not student_n:
            raise HTTPException(status_code=404, detail="Student data doesn't exist")
        db.delete(student_n)
        db.commit()
        return ResponseModel(
            status_code=200,
            status="Success",
            Student_Id=user_id,
            data=[],
            message="Student data deleted successfully."
        )
    except Exception as e:
        return ResponseModel(
            status_code=404,
            status="Failed",
            Student_Id=user_id,
            data=str(e),
            message="Student data is not deleted ."
        )
