#!flask/bin/python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import urllib, json

class Coordinates:

    def __init__ (self, longitud, latitud):
        self.latitud = latitud
        self.longitud = longitud

    def getLatitud(self):
        return (self.latitud) # / 10000)

    def getLongitud(self):
        return (self.longitud) # / -1000000)
