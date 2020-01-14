#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, Response, jsonify, json
from flask_cors import CORS
from data.Coordinates import Coordinates
from data.Description import Description
import urllib, json

class Lane:

    def __init__(self):
        self.laneList = list()

        url = "https://datosabiertos.malaga.eu/recursos/transporte/trafico/da_carrilesBici-25830.geojson"
        response = urllib.request.urlopen(url)

        if response.status >= 400:
            raise RuntimeError('Error with the request. Error code:' + response.status_code, response.status_code)

        self.data = response.read()
        features = json.loads(self.data)['features']

        for feature in features:
            id = feature['id']
            ogc_fid = feature['properties']['ogc_fid']
            name = feature['properties']['name']
            description = Description(feature['properties']['description']).getDescription()
            coordinates = list()
            #Málaga longitud=-4 latitud=36
            geometries = feature['geometry']['coordinates']
            if feature['geometry']['type'] == 'Point':
                coordenadas = Coordinates(latitud = geometries[0],longitud = geometries[1])
                coordinates.append({'latitud':coordenadas.getLatitud(),'longitud':coordenadas.getLongitud()})
            elif feature['geometry']['type'] == 'LineString':
                for  geometry in geometries:
                    coordenadas = Coordinates(geometry[0],geometry[1])
                    coordinates.append({'latitud':coordenadas.getLatitud(),'longitud':coordenadas.getLongitud()})
            self.laneList.append({'name':name,'id':id,'ogc_fid':ogc_fid,'description':description,'coordinates':coordinates,'type':feature['geometry']['type']})

    def get_geojson(self):
        return self.data

    def get_lanes(self):
        return self.laneList

    def count(self):
        print(len(self.laneList))
        return len(self.laneList)

    def get_list_names(self):
        namesList = list()
        for lane in self.laneList:
            namesList.append({'id':lane['id'],'name':lane['name']})
        return namesList

    def get_list_id_names(self):
        namesList = list()
        for lane in self.laneList:
            namesList.append({'ogc_fid':lane['ogc_fid'],'name':lane['name']})
        return namesList

    def find_by_id(self, id):
        index = 0
        while index < len(self.laneList):
            if self.laneList[index]['id'] == id:
                return self.laneList[index]
            index +=1
        raise ValueError('Bici lane id not found')

    def get_point_lanes(self):
        index = 0
        laneList = list()
        while index < len(self.laneList):
            if self.laneList[index]['type'] == 'Point':
                laneList.append(self.laneList[index])
            index +=1
        return laneList

    def get_linestring_lanes(self):
        index = 0
        laneList = list()
        while index < len(self.laneList):
            if self.laneList[index]['type'] == 'LineString':
                laneList.append(self.laneList[index])
            index +=1
        return laneList

    def find_by_ogc_fid(self, id):
        index = 0
        while index < len(self.laneList):
            if self.laneList[index]['ogc_fid'] == id:
                return self.laneList[index]
            index +=1
        raise ValueError('Bici lane ogc-fid not found')

    def get_list_coordinates(self, id):
        index = 0
        coordList = list()
        while index < len(self.laneList):
            if self.laneList[index]['ogc_fid'] == id:
                for coordinate in self.laneList[index]['coordinates']:
                    coordList.append(coordinate)
                return coordList
            index +=1
        raise ValueError('Bici lane ogc-fid not found')

    def get_description(self, id):
        index = 0
        while index < len(self.laneList):
            if self.laneList[index]['ogc_fid'] == id:
                return self.laneList[index]['description'][0]['description']
            index +=1
        raise ValueError('Bici lane ogc-fid not found')
