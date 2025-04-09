
from sqlalchemy import *

from db import base

class Student(base):
    __tablename__ = "SSMS"
    student_id = Column(Integer, primary_key= True,  autoincrement=True)
    student_Name = Column(String(50), index=True)
    student_Father_Name = Column(String(50))
    student_Age = Column(Integer)
    student_School_Name = Column(String(50))
    student_Class = Column(Integer)
    student_Village = Column(JSON)


