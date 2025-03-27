from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, String


Base = declarative_base()


class Groups(Base):
    __tablename__ = "Groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    definition = Column(String(50))
    test_prop = Column(String(50))
    

class Blogs(Base):
    __tablename__ = "Blogs"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    about = Column(String(50))
    
    
class Labels(Base):
    __tablename__ = "Labels"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    definition = Column(String(50))
    test_prop = Column(String(50))