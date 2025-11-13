from sqlalchemy import Column, Integer, String, Text, DateTime, func, UniqueConstraint
from .database import Base

class Headline(Base):
    __tablename__="headlines"
    
    id = Column(Integer, primary_key=True,index=True)
    title= Column(String(512), nullable=False)
    url= Column(String(1024), nullable=False, unique=True)
    summary= Column(Text, default="")
    source= Column(String(256), default="")
    published_at= Column(DateTime, nullable=True)
    fetched_at= Column(DateTime,server_default=func.now(), nullable=False)
    