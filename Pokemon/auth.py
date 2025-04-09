from datetime import timedelta,datetime
from typing import Annotated

from fastapi import APIRouter
from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy.util import deprecated

router = APIRouter(
    prefix="\auth",
    tags=['auth']
)

SECRET_KEY = 'Ca8bu7ktkq'
ALGORITHMS= 'HS256'

bcrypt_contex = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
