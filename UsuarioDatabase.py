import sqlite3
from sqlite3 import Error
from flask import Flask, request, Response, jsonify, json
import urllib, json


class UsuarioDatabase:

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
        query = "CREATE TABLE if not exists usuario(id_usuario integer PRIMARY KEY, name text NOT NULL, email text NOT NULL UNIQUE, role text NOT NULL, photo blob)"
        self.cursorObj.execute(query)
        self.con.commit()

    def sql_insert(self,entities,id):
        query = "INSERT INTO usuario(id_usuario, name, email, role, photo) VALUES(?, ?, ?, ?, null)"
        self.cursorObj.execute(query,entities)
        self.con.commit()
        self.sql_update_photo('imagen.jpg', id)
        response = self.sql_find(id)
        if len(response)==0:
            raise ValueError(['Operation not realized',"412"])
        return len(response)

    def sql_update_name(self,new_name,id):
        query = "UPDATE usuario SET name = \"" + str(new_name) + "\" where id_usuario = " + str(id)
        self.cursorObj.execute(query)
        self.con.commit()
        response = self.sql_get_name(id)
        return str(response) == str(new_name)

    def sql_get_name(self,id):
        lista = list()
        query = "SELECT name FROM usuario WHERE id_usuario = " + str(id)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['User not found',"404"])
        for row in rows:
            lista.append(row)
        return lista[0][0]

    def sql_get_photo(self,id):
        lista = list()
        query = "SELECT photo FROM usuario WHERE id_usuario = " + str(id)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['User not found',"404"])
        for row in rows:
            lista.append(row)
        return lista[0][0]

    def sql_update_email(self,new_email,id):
        query = "UPDATE usuario SET email = \"" + str(new_email) + "\" where id_usuario = " + str(id)
        self.cursorObj.execute(query)
        self.con.commit()
        response = self.sql_get_email(id)
        return str(response) == str(new_email)

    def sql_get_email(self,id):
        lista = list()
        query = "SELECT email FROM usuario WHERE id_usuario = " + str(id)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['User not found',"404"])
        for row in rows:
            lista.append(row)
        return lista[0][0]

    def sql_update_role(self,new_role,id):
        query = "UPDATE usuario SET role = \"" + str(new_role) + "\" where id_usuario = " + str(id)
        self.cursorObj.execute(query)
        self.con.commit()
        response = self.sql_get_role(id)
        return str(response) == str(new_role)

    def sql_update_photo(self,filename,id):
        query = "UPDATE usuario SET photo = x\'" + str(self.convertToBinaryData(filename).hex()) + "\' where id_usuario = " + str(id)
        self.cursorObj.execute(query)
        self.con.commit()
        response = self.sql_get_photo(id)
        return self.convertToBinaryData(filename) == response

    def sql_update_photo_from_blob(self,blob,id):
        query = "UPDATE usuario SET photo = x\'" + blob + "\' where id_usuario = " + str(id)
        self.cursorObj.execute(query)
        self.con.commit()
        response = self.sql_get_photo(id)
        return blob == response

    def sql_get_role(self,id):
        lista = list()
        query = "SELECT role FROM usuario WHERE id_usuario = " + str(id)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['User not found',"404"])
        for row in rows:
            lista.append(row)
        return lista[0][0]

    def sql_find_all(self):
        lista = list()
        query = "SELECT * FROM usuario"
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['Users not found',"404"])
        for row in rows:
            lista.append(row)
        return lista

    def sql_find(self,id):
        lista = list()
        query = "SELECT * FROM usuario WHERE id_usuario = " + str(id)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['User not found',"404"])
        for row in rows:
            lista.append(row)
        return lista

    def sql_find_email(self,email):
        lista = list()
        query = "SELECT * FROM usuario WHERE email = " + str(email)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['User not found',"404"])
        for row in rows:
            lista.append(row)
        return lista

    def sql_find_name(self,name):
        lista = list()
        patron = str('\"%') + name + str('%\"')
        patron.lower()
        print('El patron es: ' + patron)
        query = "SELECT * FROM usuario WHERE lower(name) LIKE " + patron
        print(query)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['User not found',"404"])
        for row in rows:
            lista.append(row)
        return lista

    def sql_find_between(self,id_from,id_to):
        lista = list()
        query = "SELECT * FROM usuario WHERE id_usuario >= " + str(id_from) + " and id_usuario <= " + str(id_to)
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if not rows:
            raise ValueError(['User not found',"404"])
        for row in rows:
            lista.append(row)
        return lista

    def sql_count(self):
        lista = list()
        response = self.sql_find_all()
        return len(response)

    def sql_remove(self,id):
        query = "DELETE FROM usuario WHERE id_usuario = "  + str(id)
        response = self.cursorObj.execute(query).rowcount
        self.con.commit()
        if response == 0:
            raise ValueError(['User not found',"404"])
        return response

    def sql_close(self):
        self.con.close()

    def sql_get_last_id(self):
        last_index = 0;
        query = "SELECT max(id_usuario) FROM usuario"
        self.cursorObj.execute(query)
        rows = self.cursorObj.fetchall()
        if rows:
            for row in rows:
                last_index = row
        return last_index[0]

    def convertToBinaryData(self, filename):
        #Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def writeTofile(self, data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")

if __name__ == '__main__':
    db = Database('iweb.db')
    db.sql_connection()
    db.sql_table()
