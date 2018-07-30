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
        self.commit_list = []
        self.commit_count = 0
        self.page_number = 1
        self.pages = True
        
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

        ############################################################################################
        """Total number of commit contributions to any project to which a user has a contributed."""
        ############################################################################################
    def ranking1(self):
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


        ############################################################################################
        """Total number of commit contributions as above, but restricted to projects that are 
        members of the original submitted set."""
        ############################################################################################
    def ranking2(self):
                
        for j in range(0,len(self.git_username)):
            self.commit_list = []
            self.page_number = 1
            self.pages = True
            while (self.pages):
                link = requests.get("https://api.github.com/repos/"+self.git_username[j]+"/"+self.git_repo[j]+"/commits?page={}&per_page=100".format(self.page_number), auth=('username', 'password'))
                json_data = json.loads(link.text)
            
                if (len(json_data) == 0):
                    self.pages = False
                    break
                
                for i in json_data:
                    
                    if(i['author'] is not None and i['author']['login'] == self.git_username[j]):
                        self.commit_list.append(i['sha'])
                    else:
                        continue
                else:
                    self.page_number = self.page_number + 1
                print( "commits by: ",self.git_username[j], len(self.commit_list) )
        ############################################################################################
        """ The number of known programming languages for each user (presuming that the languages of
        any repository committed to are known to the user) """
        ############################################################################################   
    def ranking3(self):
        for j in range(0,len(self.git_username)):
            link = requests.get("https://api.github.com/users/"+self.git_username[j]+"/repos", auth=('vimanyuK', 'Pixel2018*('))
            json_data = json.loads(link.text)
            results = nested_lookup(key = 'full_name', document = json_data, wild = True, with_keys = False)
          
            self.git_language = {}
            new = []
            for l in range(0,len(results)):
                link = requests.get("https://api.github.com/repos/"+results[l]+"/languages", auth=('vimanyuK', 'Pixel2018*('))
                language_data = json.loads(link.text)
                for x in range(0,len(language_data)):
                    new.append(list(language_data)[x])

                self.git_language['{0}'.format(self.git_username[j])] = list(set(new))
            print(self.git_language)
        

if __name__ == "__main__":
    Git = main()
    Git.ranking3()
    app.run(port = 8080)

