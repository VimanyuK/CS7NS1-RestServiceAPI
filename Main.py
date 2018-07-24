#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:17:14 2018

@author: vimanyu
"""

from flask import Flask
from flask_restful import Resource,Api, reqparse
import os,sys,requests,time, json

app = Flask(__name__)
api = Api(app)

class main():
    def __init__(self):
        self.number_of_users = input ('Enter the number username/repos you want to enter: ')
        
        
if __name__ == "__main__":
    Git = main()
    app.run(port = 8080)
        
        