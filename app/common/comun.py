from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from ..database.settings import SessionLocal

Base = declarative_base()

class common_params(Base):
    __tablename__ = "common_params"
    
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    module = Column(String, nullable=False)
    descripcion = Column(String)

Base.metadata.create_all(bind=SessionLocal().get_bind())