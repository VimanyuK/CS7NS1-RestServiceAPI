#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:17:14 2018

@author: vimanyu
"""

from flask import Flask
from flask_restful import Resource,Api, reqparse
import requests,json

app = Flask(__name__)
api = Api(app)

class main():
    def __init__(self):
        self.number_of_users = int(input ('Enter the number username/repos you want to enter: '))
        self.git_username = []
        self.git_repo = []
        
        while(self.number_of_users != 0):
            self.user_name = input('Enter the user name: ')
            self.git_username.append(self.user_name)
            self.repo_name = input('Enter the repository name: ')
            self.git_repo.append(self.repo_name)
            self.number_of_users = self.number_of_users - 1
        
        self.git_data = {}
        for n in range(0,len(self.git_username)):
            user = requests.get('https://api.github.com/repos/'+ self.git_username[n] +'/' + self.git_repo[n] + '/commits')
            self.git_data['{0}'.format(self.git_username[n])] = json.loads(user.text)
#            git_data = json.loads(user.text)
            print(self.git_data)
    
if __name__ == "__main__":
    Git = main()
    app.run(port = 8080)
        
        
    
    
    

            
            
            