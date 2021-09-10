from flaskr.modelos.modelos import AlbumSchema
from flask_restful import Resource
from ..modelos import db, Cancion, CancionSchema, Album, AlbumSchema, Usuario, UsuarioSchema
from flask import request
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from ..tareas import registrar_log

cancion_schema = CancionSchema()
album_schema = AlbumSchema()
usuario_schema = UsuarioSchema()


class VistaCanciones (Resource):

    def get(self):
        return [cancion_schema.dump(cancion) for cancion in Cancion.query.all()]

    def post(self):
        nueva_cancion = Cancion(titulo=request.json['titulo'], minutos=request.json['minutos'], segundos=request.json['segundos'], interprete=request.json['interprete'] )
        db.session.add(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)

class VistaCancion(Resource):

    def get(self, id_cancion):
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion))
    
    def put (self,id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        cancion.titulo = request.json.get('titulo', cancion.titulo)
        cancion.minutos = request.json.get('minutos', cancion.minutos)
        cancion.segundos = request.json.get('segundos', cancion.segundos)
        cancion.interprete = request.json.get('interprete', cancion.interprete)
        db.session.commit()
        return cancion_schema.dump(cancion)
    
    def delete(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        db.session.delete(cancion)
        db.session.commit()
        return 'Operacion exitosa', 204

class VistaAlbumesUsuario (Resource):

    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [album_schema.dump(album) for album in usuario.albumes]

    def post(self, id_usuario):
        nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"], descripcion=request.json["descripcion"], medio=request.json["medio"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.albumes.append(nuevo_album)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre',409

        return album_schema.dump(nuevo_album)

class VistaCancionesAlbum(Resource):

    def post(self, id_album):
        album = Album.query.get_or_404(id_album)
        
        if "id_cancion" in request.json.keys():
            
            nueva_cancion = Cancion.query.get(request.json["id_cancion"])
            if nueva_cancion is not None:
                album.canciones.append(nueva_cancion)
                db.session.commit()
            else:
                return 'Canción errónea',404
        else: 
            nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"])
            album.canciones.append(nueva_cancion)
        db.session.commit()
        return cancion_schema.dump(nueva_cancion)
       
    def get(self, id_album):
        album = Album.query.get_or_404(id_album)
        return [cancion_schema.dump(ca) for ca in album.canciones]

class VistaAlbum(Resource):

    def get(self, id_album):
        return album_schema.dump(Album.query.get_or_404(id_album))
    
    def put (self,id_album):
        album = Album.query.get_or_404(id_album)
        album.titulo = request.json.get('titulo', album.titulo)
        album.anio = request.json.get('anio', album.anio)
        album.descripcion = request.json.get('descripcion', album.descripcion)
        album.medio = request.json.get('medio', album.medio)
        db.session.commit()
        return cancion_schema.dump(album)
    
    def delete(self, id_album):
        album = Album.query.get_or_404(id_album)
        db.session.delete(album)
        db.session.commit()
        return 'Operacion exitosa', 204

class VistaLogIn(Resource):
    def post(self):
            u_nombre = request.json["nombre"]
            u_contrasena = request.json["contrasena"]
            usuario = Usuario.query.filter_by(nombre=u_nombre, contrasena = u_contrasena).all()
            if usuario:
                registrar_log.delay(u_nombre, datetime.utcnow())
                return {'mensaje':'Inicio de sesión exitoso'}, 200
            else:
                return {'mensaje':'Nombre de usuario o contraseña incorrectos'}, 401


class VistaSignIn(Resource):
    
    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return 'Usuario creado exitosamente', 201

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '',204
