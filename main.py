#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, Response, jsonify, json
from flask_cors import CORS
import urllib, json
from Lane import Lane
from Parking import Parking
from ComentarioDatabase import ComentarioDatabase
from UsuarioDatabase import UsuarioDatabase
import sqlite3
import os
from datetime import date,datetime
import http.client

# http://localhost:5000

app = Flask(__name__)



if not os.path.isfile('./iweb.db'):
    #creacion de base de datos y tabla Usuario
    usuarioDB = UsuarioDatabase('iweb.db')
    usuarioDB.sql_connection()
    usuarioDB.sql_table()
    #insercion de datos
    usuarioDB.sql_insert((0,'Anonymous','anonymous@anonymous.iweb','User'),0)
    usuarioDB.sql_insert((1,'Usuario de prueba','pruebaparaingweb@gmail.com','Admin'),1)
    usuarioDB.sql_insert((2,'Cristian Rafael Avila Garcia','avilavt@gmail.com','Admin'),2)
    usuarioDB.sql_insert((3,'Akalay Alaeak','alaeak.aa@gmail.com','Admin'),3)
    usuarioDB.sql_insert((4,'Usuario Inventado','usuario@unknown.dot','User'),4)
    #creacion de tabla Comentario
    comentarioDB = ComentarioDatabase('iweb.db')
    comentarioDB.sql_connection()
    comentarioDB.sql_table()
    #insercion de comentario 'Sin comentarios'
    comentarioDB.sql_insert((0,datetime.date(2019,12,17),'Without commentaries',0.0,0.0,0,'Empty'),0)
    usuarioDB.sql_close()
    comentarioDB.sql_close()


@app.route('/', methods=['GET'])
def holaMundo():
    datos = json.dumps({'texto':'Hola mundo'});
    return Response(datos, mimetype='application/json', status=200)

#Informacion meteorlogica

#url por defecto: http://127.0.0.1:5000/IWeb/weather/
@app.route('/IWeb/weather/', methods=['GET'])
def get_weather():
    conn = http.client.HTTPSConnection("opendata.aemet.es")
    headers = {
        'cache-control': "no-cache"
        }
    API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJyYWZnYXIyMDc0QGdtYWlsLmNvbSIsImp0aSI6IjQzZjVlODg1LWUxY2ItNGQ0Mi04MzIyLWY2YjM0YzY3NGIzZiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTc5MDI2NTIyLCJ1c2VySWQiOiI0M2Y1ZTg4NS1lMWNiLTRkNDItODMyMi1mNmIzNGM2NzRiM2YiLCJyb2xlIjoiIn0.SJYWTIR2Rmq9aFksTy-mzJTpni09X0r6VmNZMXGq5sI"
    conn.request("GET", "https://opendata.aemet.es/opendata/api/observacion/convencional/todas/?api_key="+API_KEY, headers=headers)
    response = conn.getresponse()
    data = response.read()
    #print(data)
    url_datos = json.loads(data)
    #print(url_datos)
    url_lectura = json.dumps({'url':url_datos['datos']})
    #print(url_datos['datos'])

    #idema malaga = 6156X
    response_weather = urllib.request.urlopen(url_datos['datos'])
    data_weather = response_weather.read()
    data_json = json.loads(data_weather.decode('ISO-8859-15'))
    index = 0
    lista = list()
    while index < len(data_json) and not lista:
        if data_json[index]['idema'] == '6156X':
            lista.append(data_json[index])
        index += 1
    #print('Lista: ' + str(lista))
    '''
    #metadatos
    response_meta = urllib.request.urlopen(url_datos['metadatos'])
    metadata = response_meta.read()
    #print(metadata.decode('ISO-8859-15'))
    '''
    datos_malaga = json.dumps({'id':lista[0]['idema'],'name':lista[0]['ubi'],'latitude':lista[0]['lat'],'longitude':lista[0]['lon'],'time':lista[0]['fint'],'wind':lista[0]['vmax'],'pression':lista[0]['pres'],'humidity':lista[0]['hr'],'temp':lista[0]['ta'],'temp_min':lista[0]['tamin'],'temp_max':lista[0]['tamax']})
    return Response(datos_malaga, mimetype='application/json', status=200)

# Entidad usuario

#url por defecto: http://127.0.0.1:5000/IWeb/webresources/entity.usuario/
@app.route('/IWeb/webresources/entity.usuario/', methods=['GET'])
def find_all_user():
    try:
        lista = list()
        index = 0
        usuarioDB = UsuarioDatabase('iweb.db')
        usuarioDB.sql_connection()
        response = usuarioDB.sql_find_all()
        while index < len(response):
            usuario = {'idUsuario':response[index][0],'nombre':response[index][1],'email':response[index][2],'rol':response[index][3]}
            lista.append(usuario)
            index += 1
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        usuarioDB.sql_close()
    return Response(json.dumps(lista), mimetype='application/json', status=200)

#url por defecto: http://127.0.0.1:5000/IWeb/webresources/entity.usuario/count
@app.route('/IWeb/webresources/entity.usuario/count', methods=['GET'])
def count_user():
    try:
        usuarioDB = UsuarioDatabase('iweb.db')
        usuarioDB.sql_connection()
        response = {'total':usuarioDB.sql_count()}
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        usuarioDB.sql_close()
    return Response(json.dumps(response), mimetype='application/json', status=200)


#url por defecto http://127.0.0.1:5000/IWeb/webresources/entity.usuario/0
@app.route('/IWeb/webresources/entity.usuario/<int:id>', methods=['GET'])
def find_by_user_id(id):
    try:
        usuarioDB = UsuarioDatabase('iweb.db')
        usuarioDB.sql_connection()
        response = usuarioDB.sql_find(id)
        usuario = {'idUsuario':response[0][0],'nombre':response[0][1],'email':response[0][2],'rol':response[0][3]}
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(usuario), mimetype='application/json', status=codigo)
    finally:
        usuarioDB.sql_close()
    return Response(json.dumps(usuario), mimetype='application/json', status=200)

#url por defecto http://127.0.0.1:5000/IWeb/webresources/entity.usuario/email/"anonymous@anonymous.iweb"
@app.route('/IWeb/webresources/entity.usuario/email/<string:email>', methods=['GET'])
def find_by_user_email(email):
    try:
        usuarioDB = UsuarioDatabase('iweb.db')
        usuarioDB.sql_connection()
        response = usuarioDB.sql_find_email(email)
        usuario = {'idUsuario':response[0][0],'nombre':response[0][1],'email':response[0][2],'rol':response[0][3]}
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        usuarioDB.sql_close()
    return Response(json.dumps(usuario), mimetype='application/json', status=200)

#url por defecto http://127.0.0.1:5000/IWeb/webresources/entity.usuario/name/pRueBa
@app.route('/IWeb/webresources/entity.usuario/name/<string:name>', methods=['GET'])
def find_by_user_name(name):
    try:
        usuarioDB = UsuarioDatabase('iweb.db')
        usuarioDB.sql_connection()
        response = usuarioDB.sql_find_name(name)
        usuario = {'idUsuario':response[0][0],'nombre':response[0][1],'email':response[0][2],'rol':response[0][3]}
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        usuarioDB.sql_close()
    return Response(json.dumps(usuario), mimetype='application/json', status=200)

#url por defecto http://127.0.0.1:5000/IWeb/webresources/entity.usuario/id/1/3
@app.route('/IWeb/webresources/entity.usuario/id/<int:id_from>/<int:id_to>', methods=['GET'])
def find_by_user_from_to(id_from,id_to):
    try:
        lista = list()
        index = 0
        usuarioDB = UsuarioDatabase('iweb.db')
        usuarioDB.sql_connection()
        response = usuarioDB.sql_find_between(id_from, id_to)
        while index < len(response):
            usuario = {'idUsuario':response[index][0],'nombre':response[index][1],'email':response[index][2],'rol':response[index][3]}
            lista.append(usuario)
            index += 1
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        usuarioDB.sql_close()
    return Response(json.dumps(lista), mimetype='application/json', status=200)


#formato json valido para la entrada: {"nombre":"nombre","email":"email","rol":"rol"}
#url por defecto: http://127.0.0.1:5000/IWeb/webresources/entity.usuario/post/
@app.route('/IWeb/webresources/entity.usuario/post/', methods=['POST'])
def create_user():
    print('Request = ' + str(request.json))
    if not request.json or not 'email' in request.json or not 'nombre' in request.json or not 'rol' in request.json :
        return Response(json.dumps({400:str('Bad request: '+str(request.json))}), mimetype='application/json', status=400)
    try:
        usuarioDB = UsuarioDatabase('iweb.db')
        usuarioDB.sql_connection()
        id = usuarioDB.sql_get_last_id()+1
        print('Ultimo id actual : ' + str(usuarioDB.sql_get_last_id()))
        print('Id nuevo: ' + str(id))
        usuarioDB.sql_insert((id,request.json['nombre'],request.json['email'],request.json['rol']), id)
        response = usuarioDB.sql_find(id)
        usuario = {'idUsuario':response[0][0],'nombre':response[0][1],'email':response[0][2],'rol':response[0][3]}
    except sqlite3.IntegrityError as interr:
        mensaje = interr.args
        codigo = 400
        response = {codigo: mensaje, 'id':id}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        usuarioDB.sql_close()
    return Response(json.dumps(usuario), mimetype='application/json', status=201)

#url por defecto: http://127.0.0.1:5000/IWeb/webresources/entity.usuario/{id}
@app.route('/IWeb/webresources/entity.usuario/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        usuarioDB = UsuarioDatabase('iweb.db')
        usuarioDB.sql_connection()
        response = usuarioDB.sql_remove(id)
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        usuarioDB.sql_close()
    return Response(json.dumps({'201':'User removed'}), mimetype='application/json', status=201)


# Entidad comentario

#url por defecto: http://127.0.0.1:5000/IWeb/webresources/entity.comentario/
@app.route('/IWeb/webresources/entity.comentario/', methods=['GET'])
def find_all_comentario():
    try:
        lista = list()
        index = 0
        comentarioDB = ComentarioDatabase('iweb.db')
        comentarioDB.sql_connection()
        response = comentarioDB.sql_find_all()
        while index < len(response):
            comentario = {'idComentario':response[index][0],'fechaCreacion':response[index][1],'contenido':response[index][2],'latitud':response[index][3],'longitud':response[index][4],'idUsuario':response[index][5],'tipoDato':response[index][6]}
            lista.append(comentario)
            index += 1
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        comentarioDB.sql_close()
    return Response(json.dumps(lista), mimetype='application/json', status=200)

#url por defecto: http://127.0.0.1:5000/IWeb/webresources/entity.comentario/count
@app.route('/IWeb/webresources/entity.comentario/count', methods=['GET'])
def count_comentario():
    try:
        comentarioDB = ComentarioDatabase('iweb.db')
        comentarioDB.sql_connection()
        response = {'total':comentarioDB.sql_count()}
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        comentarioDB.sql_close()
    return Response(json.dumps(response), mimetype='application/json', status=200)

#url por defecto: http://127.0.0.1:5000/IWeb/webresources/entity.comentario/count/0
@app.route('/IWeb/webresources/entity.comentario/count/<int:id>', methods=['GET'])
def count_comentario_by_user(id):
    try:
        comentarioDB = ComentarioDatabase('iweb.db')
        comentarioDB.sql_connection()
        response = {'total':comentarioDB.sql_count_by_user(id)}
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        comentarioDB.sql_close()
    return Response(json.dumps(response), mimetype='application/json', status=200)


#url por defecto http://127.0.0.1:5000/IWeb/webresources/entity.comentario/0
@app.route('/IWeb/webresources/entity.comentario/<int:id>', methods=['GET'])
def find_by_comentario_id(id):
    try:
        comentarioDB = ComentarioDatabase('iweb.db')
        comentarioDB.sql_connection()
        response = comentarioDB.sql_find(id)
        comentario = {'idComentario':response[0][0],'fechaCreacion':response[0][1],'contenido':response[0][2],'latitud':response[0][3],'longitud':response[0][4],'idUsuario':response[0][5],'tipoDato':response[0][6]}
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(usuario), mimetype='application/json', status=codigo)
    finally:
        comentarioDB.sql_close()
    return Response(json.dumps(comentario), mimetype='application/json', status=200)

#url por defecto http://127.0.0.1:5000/IWeb/webresources/entity.comentario/email/"anonymous@anonymous.iweb"
@app.route('/IWeb/webresources/entity.comentario/email/<string:email>', methods=['GET'])
def find_by_comentario_email(email):
    try:
        lista = list()
        index = 0
        usuarioDB = UsuarioDatabase('iweb.db')
        usuarioDB.sql_connection()
        resp = usuarioDB.sql_find_email(email)
        id_usuario = resp[0][0]
        comentarioDB = ComentarioDatabase('iweb.db')
        comentarioDB.sql_connection()
        response = comentarioDB.sql_get_by_id_usuario(id_usuario)
        while len(response) != 0 and index < len(response):
            comentario = {'idComentario':response[index][0],'fechaCreacion':response[index][1],'contenido':response[index][2],'latitud':response[index][3],'longitud':response[index][4],'idUsuario':response[index][5],'tipoDato':response[index][6]}
            lista.append(comentario)
            index += 1
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        comentarioDB.sql_close()
    return Response(json.dumps(lista), mimetype='application/json', status=200)

#url por defecto http://127.0.0.1:5000/IWeb/webresources/entity.comentario/contenido/primEr
@app.route('/IWeb/webresources/entity.comentario/contenido/<string:patron>', methods=['GET'])
def find_by_comentario_contenido(patron):
    try:
        comentarioDB = ComentarioDatabase('iweb.db')
        comentarioDB.sql_connection()
        response = comentarioDB.sql_find_by_contenido(patron)
        comentario = {'idComentario':response[0][0],'fechaCreacion':response[0][1],'contenido':response[0][2],'latitud':response[0][3],'longitud':response[0][4],'idUsuario':response[0][5],'tipoDato':response[0][6]}
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        comentarioDB.sql_close()
    return Response(json.dumps(comentario), mimetype='application/json', status=200)

#url por defecto http://127.0.0.1:5000/IWeb/webresources/entity.comentario/id/1/3
@app.route('/IWeb/webresources/entity.comentario/id/<int:id_from>/<int:id_to>', methods=['GET'])
def find_by_comentario_from_to(id_from,id_to):
    try:
        lista = list()
        index = 0
        comentarioDB = ComentarioDatabase('iweb.db')
        comentarioDB.sql_connection()
        response = comentarioDB.sql_find_between(id_from, id_to)
        while index < len(response):
            comentario = {'idComentario':response[index][0],'fechaCreacion':response[index][1],'contenido':response[index][2],'latitud':response[index][3],'longitud':response[index][4],'idUsuario':response[index][5],'tipoDato':response[index][6]}
            lista.append(comentario)
            index += 1
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        comentarioDB.sql_close()
    return Response(json.dumps(lista), mimetype='application/json', status=200)

#formato json valido para la entrada: {"contenido":"Mensaje generado en postman","idUsuario":1}
#url por defecto: http://127.0.0.1:5000/IWeb/webresources/entity.comentario/
@app.route('/IWeb/webresources/entity.comentario/', methods=['POST'])
def create_comentario():
    #print('Request = ' + str(request.json))
    if not request.json or not 'contenido' in request.json or not 'idUsuario' in request.json:
        return Response(json.dumps({400:str('Bad request: '+str(request.json))}), mimetype='application/json', status=400)
    try:
        if 'fechaCreacion' not in request.json:
            fechaCreacion = date.today()
        else:
            fechaCreacion = request.json['fechaCreacion']
        if 'latitud' not in request.json:
            latitud = 0.0
        else:
            latitud = request.json['latitud']
        if 'longitud' not in request.json:
            longitud = 0.0
        else:
            longitud = request.json['longitud']
        if 'tipoDato' not in request.json:
            tipoDato = 'Empty'
        else:
            tipoDato = request.json['tipoDato']
        comentarioDB = ComentarioDatabase('iweb.db')
        comentarioDB.sql_connection()
        id = comentarioDB.sql_get_last_id()+1
        comentarioDB.sql_insert((id,fechaCreacion,request.json['contenido'],latitud,longitud,request.json['idUsuario'],tipoDato), id)
        response = comentarioDB.sql_find(id)
        comentario = {'idComentario':response[0][0],'fechaCreacion':response[0][1],'contenido':response[0][2],'latitud':response[0][3],'longitud':response[0][4],'idUsuario':response[0][5],'tipoDato':response[0][6]}
    except sqlite3.IntegrityError as interr:
        mensaje = interr.args
        codigo = 400
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        comentarioDB.sql_close()
    return Response(json.dumps(comentario), mimetype='application/json', status=201)

#url por defecto: http://127.0.0.1:5000/IWeb/webresources/entity.comentario/{id}
@app.route('/IWeb/webresources/entity.comentario/<int:id>', methods=['DELETE'])
def delete_comentario(id):
    try:
        comentarioDB = ComentarioDatabase('iweb.db')
        comentarioDB.sql_connection()
        response = comentarioDB.sql_remove(id)
    except ValueError as exc:
        mensaje = exc.args[0][0]
        codigo = int(exc.args[0][1])
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    finally:
        comentarioDB.sql_close()
    return Response(json.dumps({'201':'Commentary removed'}), mimetype='application/json', status=201)



# URL = "https://datosabiertos.malaga.eu/recursos/transporte/trafico/da_carrilesBici-4326.geojson"

# Consultas sin parametros

@app.route('/opendata/api/bicilane', methods=['GET']) #url http://localhost:5000/opendata/api/bicilane
def get_lanes():
    try:
      laneList = Lane()
    except RuntimeError as exc:
      mensaje, codigo = exc.args
      response = {codigo: mensaje}
      return Response(json.dumps(response), mimetype='application/json', status=codigo)
    return Response(json.dumps(laneList.get_lanes()), mimetype='application/json', status=200)

@app.route('/opendata/api/bicilane/point', methods=['GET']) #url http://localhost:5000/opendata/api/bicilane/point
def get_point_lanes():
    try:
      laneList = Lane()
    except RuntimeError as exc:
      mensaje, codigo = exc.args
      response = {codigo: mensaje}
      return Response(json.dumps(response), mimetype='application/json', status=codigo)
    return Response(json.dumps(laneList.get_point_lanes()), mimetype='application/json', status=200)

@app.route('/opendata/api/bicilane/linestring', methods=['GET']) #url http://localhost:5000/opendata/api/bicilane/linestring
def get_linestring_lanes():
    try:
      laneList = Lane()
    except RuntimeError as exc:
      mensaje, codigo = exc.args
      response = {codigo: mensaje}
      return Response(json.dumps(response), mimetype='application/json', status=codigo)
    return Response(json.dumps(laneList.get_linestring_lanes()), mimetype='application/json', status=200)

@app.route('/opendata/api/bicilane/count', methods=['GET']) #url http://localhost:5000/opendata/api/bicilane/count
def get_lane_count():
    try:
      laneList = Lane()
    except RuntimeError as exc:
      mensaje, codigo = exc.args
      response = {codigo: mensaje}
      return Response(json.dumps(response), mimetype='application/json', status=codigo)
    return Response(json.dumps({'count':laneList.count()}), mimetype='application/json', status=200)

@app.route('/opendata/api/bicilane/list_names', methods=['GET']) #url http://localhost:5000/opendata/api/bicilane/list_names
def get_lanes_list_names():
    try:
      laneList = Lane()
    except RuntimeError as exc:
      mensaje, codigo = exc.args
      response = {codigo: mensaje}
      return Response(json.dumps(response), mimetype='application/json', status=codigo)
    return Response(json.dumps(laneList.get_list_names()), mimetype='application/json', status=200)

@app.route('/opendata/api/bicilane/list_id_names', methods=['GET']) #url http://localhost:5000/opendata/api/bicilane/list_id_names
def get_lanes_list_id_names():
    try:
      laneList = Lane()
    except RuntimeError as exc:
      mensaje, codigo = exc.args
      response = {codigo: mensaje}
      return Response(json.dumps(response), mimetype='application/json', status=codigo)
    return Response(json.dumps(laneList.get_list_id_names()), mimetype='application/json', status=200)

@app.route('/opendata/api/bicilane/list_coordinates_zero', methods=['GET']) #url http://localhost:5000/opendata/api/bicilane/list_coordinates_zero
def get_lanes_list_coordinates_zero():
    try:
      laneList = Lane()
    except RuntimeError as exc:
      mensaje, codigo = exc.args
      response = {codigo: mensaje}
      return Response(json.dumps(response), mimetype='application/json', status=codigo)
    return Response(json.dumps(laneList.get_list_coordinates_zero()), mimetype='application/json', status=200)

# Consultas parametrizadas

#ejemplo de id: da_carrilesBici.fid--5673ced1_16ed9249c70_-4eb
@app.route('/opendata/api/bicilane/find_by_id/<string:id>', methods=['GET']) #url http://localhost:5000/opendata/api/bicilane/find_by_id/da_carrilesBici.fid--5673ced1_16ef808f022_b36
def find_lanes_by_id(id):
    try:
        laneList = Lane()
    except RuntimeError as exc:
        mensaje, codigo = exc.args
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    try:
        lane = laneList.find_by_id(id)
    except ValueError:
        response = {'404':'Bici lane id \'{}\' not found'.format(id)}
        return Response(json.dumps(response), mimetype='application/json', status=404)
    return Response(json.dumps(lane), mimetype='application/json', status=200)

@app.route('/opendata/api/bicilane/find_by_ogc_fid/<int:id>', methods=['GET']) #url http://localhost:5000/opendata/api/bicilane/find_by_ogc_fid/43383
def find_lanes_by_ogc_fid(id):
    try:
        laneList = Lane()
    except RuntimeError as exc:
        mensaje, codigo = exc.args
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    try:
        lane = laneList.find_by_ogc_fid(id)
    except ValueError:
        response = {'404':'Bici lane ogc-fid {} not found'.format(id)}
        return Response(json.dumps(response), mimetype='application/json', status=404)
    return Response(json.dumps(lane), mimetype='application/json', status=200)


@app.route('/opendata/api/bicilane/get_list_coordinates/<int:id>', methods=['GET']) #url http://localhost:5000/opendata/api/bicilane/get_list_coordinates/43383
def get_lanes_list_coordinates(id):
    try:
        laneList = Lane()
    except RuntimeError as exc:
        mensaje, codigo = exc.args
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    try:
        lane = laneList.get_list_coordinates(id)
    except ValueError:
        response = {'404':'Bici lane ogc-fid {} not found'.format(id)}
        return Response(json.dumps(response), mimetype='application/json', status=404)
    return Response(json.dumps(lane), mimetype='application/json', status=200)

@app.route('/opendata/api/bicilane/get_description/<int:id>', methods=['GET']) #url http://localhost:5000/opendata/api/bicilane/get_description/43383
def get_lanes_description(id):
    try:
        laneList = Lane()
    except RuntimeError as exc:
        mensaje, codigo = exc.args
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    try:
        lane = laneList.get_description(id)
    except ValueError:
        response = {'404':'Bici lane ogc-fid {} not found'.format(id)}
        return Response(json.dumps(response), mimetype='application/json', status=404)
    return Response(json.dumps(lane), mimetype='application/json', status=200)


# URL = " https://datosabiertos.malaga.eu/recursos/transporte/trafico/da_aparcamientosBici-4326.geojson"

# Consultas sin parametros

@app.route('/opendata/api/bicipark', methods=['GET']) #url http://localhost:5000/opendata/api/bicipark
def get_parkings():
    try:
      parkList = Parking()
    except RuntimeError as exc:
      mensaje, codigo = exc.args
      response = {codigo: mensaje}
      return Response(json.dumps(response), mimetype='application/json', status=codigo)
    return Response(json.dumps(parkList.get_parkings()), mimetype='application/json', status=200)

# Consultas parametrizadas

#ejemplo de id: "da_aparcamientosBici.fid--5673ced1_16f07759926_25c9"
@app.route('/opendata/api/bicipark/find_by_id/<string:id>', methods=['GET']) #url http://localhost:5000/opendata/api/bicipark/find_by_id/da_aparcamientosBici.fid--5673ced1_16f07759926_25c9
def find_parking_by_id(id):
    try:
        parkList = Parking()
    except RuntimeError as exc:
        mensaje, codigo = exc.args
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    try:
        parking = parkList.find_by_id(id)
    except ValueError:
        response = {'404':'Bici Parking id \'{}\' not found'.format(id)}
        return Response(json.dumps(response), mimetype='application/json', status=404)
    return Response(json.dumps(parking), mimetype='application/json', status=200)

#ejemplo de id: "da_aparcamientosBici.fid--5673ced1_16f07759926_25c9"
@app.route('/opendata/api/bicipark/find_by_ogc_fid/<int:id>', methods=['GET']) #url http://localhost:5000/opendata/api/bicipark/find_by_ogc_fid/43526
def find_parking_by_ogc_fid(id):
    try:
        parkList = Parking()
    except RuntimeError as exc:
        mensaje, codigo = exc.args
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    try:
        parking = parkList.find_by_ogc_fid(id)
    except ValueError:
        response = {'404':'Bici Parking id \'{}\' not found'.format(id)}
        return Response(json.dumps(response), mimetype='application/json', status=404)
    return Response(json.dumps(parking), mimetype='application/json', status=200)

@app.route('/opendata/api/bicipark/get_description/<int:id>', methods=['GET']) #url http://localhost:5000/opendata/api/bicipark/get_description/43383
def get_parking_description(id):
    try:
        parkList = Parking()
    except RuntimeError as exc:
        mensaje, codigo = exc.args
        response = {codigo: mensaje}
        return Response(json.dumps(response), mimetype='application/json', status=codigo)
    try:
        parking = parkList.get_description(id)
    except ValueError:
        response = {'404':'Bici parking ogc-fid {} not found'.format(id)}
        return Response(json.dumps(response), mimetype='application/json', status=404)
    return Response(json.dumps(parking), mimetype='application/json', status=200)


if __name__ == '__main__':
    #app.run(host="127.0.0.1", port=8000, debug=True)
    app.run(debug=True)
