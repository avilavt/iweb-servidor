from UsuarioDatabase import UsuarioDatabase
from ComentarioDatabase import ComentarioDatabase
import os
import datetime

if not os.path.isfile('./iweb.db'):
    #creación de base de datos y tabla Usuario
    usuarioDB = UsuarioDatabase('iweb.db')
    usuarioDB.sql_connection()
    usuarioDB.sql_table()
    #inserción de datos
    usuarioDB.sql_insert((0,'Anonymous','anonymous@anonymous.iweb','User'),0)
    usuarioDB.sql_insert((1,'Usuario de prueba','pruebaparaingweb@gmail.com','Admin'),1)
    usuarioDB.sql_insert((2,'Cristian Rafael Ávila García','avilavt@gmail.com','Admin'),2)
    usuarioDB.sql_insert((3,'Akalay Alaeak','alaeak.aa@gmail.com','Admin'),3)
    usuarioDB.sql_insert((4,'Usuario Inventado','usuario@unknown.dot','User'),4)
    #creación de tabla Comentario
    comentarioDB = ComentarioDatabase('iweb.db')
    comentarioDB.sql_connection()
    comentarioDB.sql_table()
    #inserción de comentario 'Sin comentarios'
    comentarioDB.sql_insert((0,datetime.date(2019,12,17),'Without commentaries',0.0,0.0,0,'Empty'),0)
    usuarioDB.sql_close()
    comentarioDB.sql_close()

usuarioDB = UsuarioDatabase('iweb.db')
usuarioDB.sql_connection()
print('Last id: ' + str(usuarioDB.sql_get_last_id()))
print('Find by name: ' + str(usuarioDB.sql_find_name("tIaN")))
print('Find between 1 and 3: ' + str(usuarioDB.sql_find_between(1,3)))
#Prueba para usuarioDatabase
'''
usuarioDB = UsuarioDatabase('iweb.db')
usuarioDB.sql_connection()
print('Update name: ' + str(usuarioDB.sql_update_name("Invented User", 4)))
print('Update email: ' + str(usuarioDB.sql_update_email("invented@algo.com", 4)))
print('Update role: ' + str(usuarioDB.sql_update_role("Visitor", 4)))
print('Insert: ' + str(usuarioDB.sql_insert((5,'Abc','abc','User'),5)))
print('Remove: ' + str(usuarioDB.sql_remove(5)))
print(usuarioDB.sql_find(0))
for usuario in usuarioDB.sql_find_all():
    print(usuario)
print(usuarioDB.sql_count())
'''

comentarioDB = ComentarioDatabase('iweb.db')
comentarioDB.sql_connection()
print('Comentario: ' + str(comentarioDB.sql_find(0)))
#print('Comentarios de usuario 1: ' + str(comentarioDB.sql_get_by_id_usuario(1)))
#print('Comentario que contiene pr: ' + str(comentarioDB.sql_find_by_contenido("pR")))
print('Last id: ' + str(comentarioDB.sql_get_last_id()))


#Prueba para comentarioDatabase
'''
comentarioDB = ComentarioDatabase('iweb.db')
comentarioDB.sql_connection()
print('Insert: ' + str(comentarioDB.sql_insert((1,datetime.date(2019,12,17),'no',0.0,0.0,0,'nno'), 1)))
print('Contenido: ' + str(comentarioDB.sql_get_content(1)))
print('Update contenido: ' + str(comentarioDB.sql_update_contenido('Hola, mundo', 1)))
print('Remove: ' + str(comentarioDB.sql_remove(1)))
print(comentarioDB.sql_find(0))
for comentario in comentarioDB.sql_find_all():
    print(comentario)
print(comentarioDB.sql_count())
'''
