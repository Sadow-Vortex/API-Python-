from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = 'mysql+pymysql://root:rpmanna45@localhost:3306/Prayash'

engine = create_engine(DATABASE_URL, echo=True)

sessionlocal = sessionmaker(autocommit= False,autoflush= False, bind= engine)

base = declarative_base()