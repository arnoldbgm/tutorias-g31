from flask_mail import Message
from flask import render_template

# Creacion de mi funcion
def enviar_correo(to_email, usuario):
   from app import mail
   msg = Message('Bienvenido a mi app', recipients=[to_email] )
   msg.html = render_template('new_welcome.html', usuario=usuario)
   mail.send(msg)