from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from ..database.settings import SessionLocal


Base = declarative_base()

class Holidays(Base):
    __tablename__ = "Holidays"
    
    id = Column(Integer, primary_key=True, index=True)
    nombreHoliday = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    tipo = Column(String, nullable=False)
    descripcion = Column(String)
    dia_semana = Column(String, nullable=False)

Base.metadata.create_all(bind=SessionLocal().get_bind())