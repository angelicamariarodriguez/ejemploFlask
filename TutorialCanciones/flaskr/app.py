from flaskr import create_app
from .modelos import db, Cancion, Album, Usuario, Medio

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

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
    print(Album.query.all())
    print(Cancion.query.all())
    print(Album.query.all()[2].canciones)
    db.session.delete(a)
    print(Album.query.all())
    print(Cancion.query.all())

