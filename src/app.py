from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

from config import config
from validaciones import *

app = Flask(__name__)

# CORS(app)
CORS(app, resources={r"/cursos/*": {"origins": "http://localhost"}})

conexion = MySQL(app)


# @cross_origin
@app.route('/posts', methods=['GET'])
def listar_cursos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, creditos FROM post ORDER BY nombre ASC"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursos = []
        for fila in datos:
            post = {'codigo': fila[0], 'nombre': fila[1]}
            posts.append(post)
        return jsonify({'cursos': cursos, 'mensaje': "posts listados.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


def leer_post_bd(codigo):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT codigo, nombre, creditos FROM post WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            curso = {'codigo': datos[0], 'nombre': datos[1], 'creditos': datos[2]}
            return curso
        else:
            return None
    except Exception as ex:
        raise ex


@app.route('/posts/<codigo>', methods=['GET'])
def leer_curso(codigo):
    try:
        curso = leer_curso_bd(codigo)
        if curso != None:
            return jsonify({'post': post, 'mensaje': "post encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "post no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/posts', methods=['POST'])
def registrar_post():
    # print(request.json)
    if (validar_codigo(request.json['codigo']) and validar_nombre(request.json['nombre']) ):
        try:
            curso = leer_posts_bd(request.json['codigo'])
            if curso != None:
                return jsonify({'mensaje': "Código ya existe, no se puede duplicar.", 'exito': False})
            else:
                cursor = conexion.connection.cursor()
                sql = """INSERT INTO post (codigo, nombre) 
                VALUES ('{0}', '{1}')""".format(request.json['codigo'],
                                                     request.json['nombre'])
                cursor.execute(sql)
                conexion.connection.commit()  # Confirma la acción de inserción.
                return jsonify({'mensaje': "Curso registrado.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})


@app.route('/posts/<codigo>', methods=['PUT'])
def actualizar_curso(codigo):
    if (validar_codigo(codigo) and validar_nombre(request.json['nombre']) and validar_creditos(request.json['creditos'])):
        try:
            curso = leer_curso_bd(codigo)
            if curso != None:
                cursor = conexion.connection.cursor()
                sql = """UPDATE post SET nombre = '{0}', creditos = {1} 
                WHERE codigo = '{2}'""".format(request.json['nombre'], request.json['creditos'], codigo)
                cursor.execute(sql)
                conexion.connection.commit()  # Confirma la acción de actualización.
                return jsonify({'mensaje': "post actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "post no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
    else:
        return jsonify({'mensaje': "Parámetros inválidos...", 'exito': False})


@app.route('/posts/<codigo>', methods=['DELETE'])
def eliminar_curso(codigo):
    try:
        curso = leer_curso_bd(codigo)
        if curso != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM curso WHERE codigo = '{0}'".format(codigo)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de eliminación.
            return jsonify({'mensaje': "post eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "post no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
