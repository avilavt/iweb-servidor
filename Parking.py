#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import urllib, json
from Description import Description
from Coordinates import Coordinates

class Parking:

    def __init__(self):
        self.parkList = list()

        url = " https://datosabiertos.malaga.eu/recursos/transporte/trafico/da_aparcamientosBici-4326.geojson"
        response = urllib.request.urlopen(url)
        self.data = response.read()
        features = json.loads(self.data)['features']

        for feature in features:
            id_parking = feature['id']
            ogc_fid = feature['properties']['ogc_fid']
            desc = Description(feature['properties']['description'])
            description = desc.getDescriptionParking()
            name = desc.getNameParking()
            coordinates = list()
            geometries = feature['geometry']['coordinates']
            if feature['geometry']['type'] == 'Point':
                coordenadas = Coordinates(latitud = geometries[1],longitud = geometries[0])
                coordinates.append({'latitud':coordenadas.getLatitud(),'longitud':coordenadas.getLongitud()})
            elif feature['geometry']['type'] == 'LineString':
                for  geometry in geometries:
                    coordenadas = Coordinates(geometry[1],geometry[0])
                    coordinates.append({'latitud':coordenadas.getLatitud(),'longitud':coordenadas.getLongitud()})
            self.parkList.append({'name':name, 'id':id_parking,'ogc_fid':ogc_fid,'description':description,'coordinates':coordinates})

    def get_parkings(self):
        return self.parkList

    def count(self):
        return {'count':len(self.parkList)}

    def get_list_names(self):
        namesList = list()
        for park in self.parkList:
            namesList.append({'id':park['id'],'name':park['name']})
        return namesList

    def get_list_id_names(self):
        namesList = list()
        for park in self.parkList:
            namesList.append({'ogc_fid':park['ogc_fid'],'name':park['name']})
        return namesList

    def find_by_id(self, id):
        index = 0
        while index < len(self.parkList):
            if self.parkList[index]['id'] == id:
                return self.parkList[index]
            index +=1
        raise ValueError(404)

    def find_by_ogc_fid(self, id):
        index = 0
        while index < len(self.parkList):
            print(self.parkList[index]['ogc_fid'])
            if self.parkList[index]['ogc_fid'] == id:
                return self.parkList[index]
            index +=1
        raise ValueError(404)

    def get_description(self, id):
        index = 0
        while index < len(self.parkList):
            if self.parkList[index]['ogc_fid'] == id:
                return self.parkList[index]['description'][0]['description']
            index +=1
        raise ValueError(404)
