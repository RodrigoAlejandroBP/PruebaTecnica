from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.database.settings import SessionLocal
from pydantic import BaseModel
from datetime import date


Base = declarative_base()

class Holidays(BaseModel): 
    __tablename__ = "Holidays"
    id: int = Column(Integer, primary_key=True, index=True) 
    nombreFeriado: str = Column(String, nullable=False)
    fecha: date = Column(Date, nullable=False)
    tipo: str = Column(String, nullable=False)
    descripcion: str = Column(String)
    dia_semana:  str = Column(String, nullable=False)
    irrenunciable: int = Column(Integer, primary_key=True, index=True) 

 
Base.metadata.create_all(bind=SessionLocal().get_bind())