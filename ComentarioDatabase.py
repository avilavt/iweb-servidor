import sqlite3
from sqlite3 import Error
import datetime
import os

class ComentarioDatabase:

    def __init__(self, database):
        self.database = database

    def sql_connection(self):
        try:
            self.con = sqlite3.connect(self.database)
            self.cursorObj = self.con.cursor()
            print("Connection is established: Database is created in memory")
        except Error:
            print(Error)

    def sql_table(self):
        query = "CREATE TABLE if not exists comentario(id_comentario integer PRIMARY KEY, fecha_creacion date NOT NULL, contenido text NOT NULL, latitude real NOT NULL, longitude real NOT NULL, id_usuario integer NOT NULL, type_data text NOT NULL)"
        self.cursorObj.execute(query)
        self.con.commit()

    def sql_insert(self,entities,id):
        query = "INSERT INTO comentario(id_comentario, fecha_creacion, contenido, latitude, longitude, id_usuario, type_data) VALUES(?, ?, ?, ?, ?, ?, ?)"
        self.cursorObj.execute(query,entities)
        self.con.commit()
        response = self.sql_find(id)
        if len(response)==0:
            raise ValueError(['Operation not realized',"412"])
        return len(response)

    def sql_update_contenido(self,new_contenido,id):
        query = "UPDATE comentario SET contenido = \"" + str(new_contenido) + "\" where id_comentario = " + str(id)
        self.cursorObj.execute(query)
        self.con.commit()
        response = self.sql_get_content(id)
        return str(response) == str(new_contenido)

    def sql_get_content(self,id):
        lista = list()
        query = "SELECT contenido FROM comentario WHERE id_comentario = " + str(id)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Commentary not found',"404"])
        for row in rows:
            lista.append(row)
        return lista[0][0]

    def sql_get_by_id_usuario(self,idUsuario):
        lista = list()
        query = "SELECT * FROM comentario WHERE id_usuario = " + str(idUsuario)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        for row in rows:
            lista.append(row)
        return lista

    def sql_find_all(self):
        lista = list()
        query = "SELECT * FROM comentario"
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Commentaries not found',"404"])
        for row in rows:
            lista.append(row)
        return lista

    def sql_find(self,id):
        lista = list()
        query = "SELECT * FROM comentario WHERE id_comentario = " + str(id)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Commentary not found',"404"])
        for row in rows:
            lista.append(row)
        return lista

    def sql_count(self):
        lista = list()
        response = self.sql_find_all()
        return len(response)

    def sql_count_by_user(self,id_usuario):
        lista = list()
        response = self.sql_get_by_id_usuario(id_usuario)
        return len(response)

    def sql_find_by_contenido(self,contenido):
        lista = list()
        patron = str('\"%') + contenido + str('%\"')
        patron.lower()
        print('El patron es: ' + patron)
        query = "SELECT * FROM comentario WHERE lower(contenido) LIKE " + patron
        print(query)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Commentary not found',"404"])
        for row in rows:
            lista.append(row)
        return lista


    def sql_find_between(self,id_from,id_to):
        lista = list()
        query = "SELECT * FROM comentario WHERE id_comentario >= " + str(id_from) + " and id_comentario <= " + str(id_to)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Commentaries not found',"404"])
        for row in rows:
            lista.append(row)
        return lista

    def sql_remove(self,id):
        query = "DELETE FROM comentario WHERE id_comentario = "  + str(id)
        response = self.cursorObj.execute(query).rowcount
        self.con.commit()
        if response == 0:
            raise ValueError(['Commentary not found',"404"])
        return response

    def sql_close(self):
        self.con.close()

    def sql_get_last_id(self):
        last_index = 0;
        query = "SELECT max(id_comentario) FROM comentario"
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if rows:
            for row in rows:
                last_index = row
        return last_index[0]

if __name__ == '__main__':
    db = Database('iweb.db')
    db.sql_connection()
    db.sql_table()
