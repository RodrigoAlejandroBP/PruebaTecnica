from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.settings import Base,SessionLocal
from pydantic import BaseModel
from datetime import date


class Holidays(Base): 
    __tablename__ = "Holidays"
    id: int = Column(Integer, primary_key=True, index=True,autoincrement=True,nullable=False) 
    nombreFeriado: str = Column(String, nullable=False)
    fecha: date = Column(Date, nullable=False)
    tipo: str = Column(String, nullable=False)
    descripcion: str = Column(String)
    dia_semana:  str = Column(String, nullable=False)
    irrenunciable: int = Column(Integer, index=True) 


##Holidays tipo puede ser una tabla con FK a holidays ... 