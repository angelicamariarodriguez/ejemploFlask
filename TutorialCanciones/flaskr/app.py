from flaskr import create_app
from .modelos import db, Cancion, Album, Usuario, Medio
from .modelos import AlbumSchema, CancionSchema, UsuarioSchema
from flask_restful import Api
from .vistas import VistaCanciones, VistaCancion, VistaSignIn, VistaAlbumesUsuario, VistaAlbum, VistaCancionesAlbum

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaCanciones, '/canciones')
api.add_resource(VistaCancion, '/canciones/<int:id_cancion>')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaAlbumesUsuario, '/usuario/<int:id_usuario>/albumes')
api.add_resource(VistaAlbum, '/album/<int:id_album>')
api.add_resource(VistaCancionesAlbum, '/album/<int:id_album>/canciones')

#PRUEBA
with app.app_context():
    c = Cancion(titulo='Prueba', minutos=2, segundos=25, interprete='Angelica')
    c2= Cancion(titulo='Prueba2', minutos=2, segundos=25, interprete='Angelica')
    db.session.add(c)
    db.session.add(c2)
    db.session.commit()
    #print(Cancion.query.all())

#PRUEBA
with app.app_context():
    m = Medio(1)
    a = Album(titulo='Prueba', anio=2000, descripcion='Esto es una prueba', medio=m)
    a2= Album(titulo='Prueba2', anio=2010, descripcion='Esto es otra prueba', medio=m)
    db.session.add(a)
    db.session.add(a2)
    db.session.commit()
    #print(Album.query.all())

#PRUEBA
with app.app_context():
    u = Usuario(nombre='Angelica', contrasenia='1234')
    u2= Usuario(nombre='Maria', contrasenia='25678')
    db.session.add(u)
    db.session.add(u2)
    db.session.commit()
    #print(Usuario.query.all())

#PRUEBA
with app.app_context():
    u = Usuario(nombre='Teresa', contrasenia='1234')
    a = Album(titulo='Hola', anio=2000, descripcion='Esto es una prueba', medio=Medio.CD)
    c = Cancion(titulo='Mi cancion', minutos=2, segundos=25, interprete='Angelica')
    u.albumes.append(a)
    a.canciones.append(c)
    db.session.add(u)
    db.session.add(c)
    db.session.commit()
    #print(Usuario.query.all())
    #print(Usuario.query.all()[2].albumes)
    #db.session.delete(u)
    #print(Usuario.query.all())
    #print(Album.query.all())
    #print(Album.query.all())
    #print(Cancion.query.all())
    #print(Album.query.all()[2].canciones)
    #db.session.delete(a)
    #print(Album.query.all())
    #print(Cancion.query.all())

#PRUEBA
with app.app_context():
    album_schema = AlbumSchema()
    a = Album(titulo='Prueba5', anio=2021, descripcion='Esto es una prueba5', medio=Medio.CD)
    db.session.add(a)
    db.session.commit()
    #print([album_schema.dumps(album) for album in Album.query.all()])

#PRUEBA
with app.app_context():
    cancion_schema = CancionSchema()
    c = Cancion(titulo='Prueba5', minutos=5, segundos=25, interprete='Angelica')
    db.session.add(c)
    db.session.commit()
    #print([cancion_schema.dumps(cancion) for cancion in Cancion.query.all()])

#PRUEBA
with app.app_context():
    usuario_schema = UsuarioSchema()
    u = Usuario(nombre='AngelicaM', contrasenia='123456')
    db.session.add(u)
    db.session.commit()
    print([usuario_schema.dumps(usuario) for usuario in Usuario.query.all()])