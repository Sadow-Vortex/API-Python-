from sqlalchemy import *
from db import base
class StudentSportAssociation(base):
    __tablename__ = "student_sport_association"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)
    sport_id = Column(Integer)
    created_by = Column(String)
    updated_by = Column(String)
