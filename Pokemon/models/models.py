from operator import index

from sqlalchemy import *
from config.db import base

class Pokemon(base):
    __tablename__ = 'Pokemons'
    id = Column(Integer,primary_key=True, index=True)
    rank = Column(Integer)
    name = Column(String(50), index=True)
    type = Column(String(50))
    strength = Column(Integer)
    speed = Column(Integer)
    health = Column(Integer)
    defence = Column(Integer)
    Power_against_increase = Column(String(50))
    description = Column(String(1000))
    Power_against_decrease = Column(String(50))
    # image =  Column(LargeBinary)
