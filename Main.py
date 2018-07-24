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
        self.number_of_users = int(input ('Enter the number username/repos you want to enter: '))
        self.git_username = []
        self.git_repo = []
        
        for n in range(0,self.number_of_users):
            self.user_name = input('Enter the user name: ')
            self.repo_name = input('Enter the repository name: ')
            self.git_username.append(self.user_name)
            self.git_repo.append(self.repo_name)
        
#        print(self.git_username)
#        print(self.git_repo)
 
        user = requests.get('https://api.github.com/repos/'+ self.git_username[0] +'/' + self.git_repo[0] + '/commits')
        git_data = json.loads(user.text)
        print(git_data)
    
if __name__ == "__main__":
    Git = main()
    app.run(port = 8080)
        
        