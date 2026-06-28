from db import db
from sqlalchemy import Column, Integer, String

class UsuariosTable(db.Model):
   __tablename__ = 'usuarios'

   id = Column(Integer, primary_key=True)
   nombre = Column(String(255), nullable=False)
   telefono = Column(String(9), nullable=True)
   correo = Column(String(255), nullable=False)
   password = Column(String(255), nullable=False)