#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:17:14 2018

@author: vimanyu
"""

from flask import Flask
from flask_restful import Resource,Api, reqparse
import requests,json, subprocess, datetime
from nested_lookup import nested_lookup

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
#            print(self.git_data)
    
        self.git_commit_count = {}
        for i in range(0,len(self.git_username)):
            git_user_data = {}
            temp = subprocess.check_output(["curl", "-H", "Accept: application/vnd.github.cloak-preview", "https://api.github.com/search/commits?q=author:"+self.git_username[i]+"&per_page=1000"], shell=False).decode('utf-8')
            git_user_data['{0}'.format(self.git_username[i])] = json.loads(temp)
            results = nested_lookup(key = 'date', document = git_user_data, wild = True, with_keys = False)
            results = list(set(results))
            results = [x for x in results if ("2018" in x)]
            self.git_commit_count['{0}'.format(self.git_username[i])] = len(results)
        print(self.git_commit_count)


if __name__ == "__main__":
    Git = main()
    app.run(port = 8080)


###### for converting unix timestamp
print(
    datetime.datetime.fromtimestamp(
        int("1531612800")
    ).strftime('%Y-%m-%d %H:%M:%S')
)
