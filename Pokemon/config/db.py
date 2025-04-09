from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_DATABASE = 'mysql+pymysql://root:rpmanna45@localhost:3306/BlogApplication'

engine = create_engine(URL_DATABASE)
sessionLocal = sessionmaker(autoflush= False, autocommit = False, bind=engine)
base = declarative_base()