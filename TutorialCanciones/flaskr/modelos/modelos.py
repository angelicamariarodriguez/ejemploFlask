from flask_sqlalchemy import SQLAlchemy
import enum 

db = SQLAlchemy()

albumes_canciones = db.Table('album_cancion',
db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True),
db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'), primary_key= True))

class Cancion(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    titulo = db.Column(db.String(128))
    minutos = db.Column(db.Integer)
    segundos = db.Column(db.Integer)
    interprete = db.Column(db.String(128))
    albumes = db.relationship('Album', secondary='album_cancion', back_populates='canciones')

    def __repr__(self):
        return "{}-{}-{}-{}".format(self.titulo, self.minutos, self.segundos, self.interprete)

class Medio(enum.Enum):
   DISCO = 1
   CASETE = 2
   CD = 3

class Album(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    titulo = db.Column(db.String(128))
    anio = db.Column(db.Integer)
    descripcion = db.Column(db.String(250))
    medio = db.Column(db.Enum(Medio))
    usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    canciones = db.relationship('Cancion', secondary='album_cancion', back_populates='albumes')
    __table__args__= (db.UniqueConstraint('usuario', 'titulo', name='titulo_unico_album'),)

    def __repr__(self):
        return "{}-{}-{}-{}".format(self.titulo, self.anio, self.descripcion, self.medio)

class Usuario(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    nombre = db.Column(db.String(128))
    contrasenia = db.Column(db.String(8))
    albumes = db.relationship('Album', cascade= 'all, delete, delete-orphan')

    def __repr__(self):
        return "{}-{}".format(self.nombre, self.contrasenia)
