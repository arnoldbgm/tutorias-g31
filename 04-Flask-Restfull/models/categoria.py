from db import db
from sqlalchemy import Column, Integer, String

#db.Model => Que aqui se va a crear una tabla
class CategoriasTable(db.Model):
   __tablename__ = "categorias" # El nombre de mi tabla en mi bd

   id = Column(Integer, primary_key=True)
   nombre = Column(String(255), nullable=False)