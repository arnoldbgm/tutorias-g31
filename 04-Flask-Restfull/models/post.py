from db import db
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

class PostTable(db.Model):
   __tablename__ = "posts"

   id = Column(Integer, primary_key=True)
   titulo = Column(String(255), nullable=False)
   contenido = Column(Text, nullable=False)
   fecha = Column(DateTime, nullable=False)
   categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False )