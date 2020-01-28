#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.setdefaultencoding('utf-8')

class Description:

    def __init__(self, description):
        self.description = description
        self.name = ""

    def getDescriptionLane(self):
        descripcion = list()
        desc = self.description.replace('<b>', '#').replace('</b>', '#').replace('<', '#').replace('>', '#').split('#')
        indexK = desc.index('Kilometros:')
        km = float(desc[indexK+1].replace('&nbsp;',' ').strip().replace(',','.'))
        indexD = desc.index('Descripcion:')
        descripcion.append({'kilometers':km,'description':desc[indexD+1].replace('&nbsp;',' ').strip()})
        return descripcion


    def getDescriptionParking(self):
        descripcion = list()
        desc = self.description.replace('<b>', '#').replace('</b>', '#').replace('<', '#').replace('>', '#').split('#')
        indexU = desc.index('Ubicación:')
        ubicacion = desc[indexU+1].replace('&nbsp;',' ').strip().replace(',',' Nº ')
        indexP = desc.index('N° Plazas: ')
        plazas = desc[indexP+1].replace('&nbsp;',' ').strip().replace(',','.')
        indexD = desc.index('Descripción:')
        descrip = desc[indexD+1].replace('&nbsp;',' ').strip().replace(',','.')
        desc = ubicacion.replace('Nº','#').split('#')
        self.name = desc[0].strip()
        descripcion.append({'ubication':ubicacion,'description':descrip.strip(),'places':plazas})
        return descripcion

    def getNameParking(self):
        return self.name
