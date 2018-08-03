#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:17:14 2018

@author: vimanyu
"""



from flask import Flask, jsonify
from flask_restful import Resource,Api, reqparse
import requests,json, subprocess, datetime
from nested_lookup import nested_lookup

app = Flask(__name__)

"""Enter username and password use the git hub api"""
Username = ""
Password = ""


class main():
    def __init__(self):
        self.number_of_users = int(input ('Enter the number username/repos you want to enter: '))
        self.git_username = []
        self.git_repo = []
        self.git_users = []
        while(self.number_of_users != 0):
            self.user_name = input('Enter the user name: ')
            self.git_username.append(self.user_name)
            self.repo_name = input('Enter the repository name: ')
            self.git_repo.append(self.repo_name)
            self.number_of_users = self.number_of_users-1
        self.git_users.append(dict(zip(self.git_username,self.git_repo)))

@app.route('/gituser',methods=['GET'])
def getAllgituser():
    return jsonify(M.git_users)

############################################################################################
"""1.Total number of commit contributions to any project to which a user has a contributed."""
############################################################################################
@app.route('/rank1',methods=['GET'])
def rank1():
    git_commit_count = {}
    for i in range(0,len(M.git_username)):
        git_user_data = {}
        temp = subprocess.check_output(["curl", "-H", "Accept: application/vnd.github.cloak-preview", "https://api.github.com/search/commits?q=author:"+M.git_username[i]+"&per_page=1000"], shell=False).decode('utf-8')
        git_user_data['{0}'.format(M.git_username[i])] = json.loads(temp)
        results = nested_lookup(key = 'date', document = git_user_data, wild = True, with_keys = False)
        results = list(set(results))
        results = [x for x in results if ("2018" in x)]
        git_commit_count['{0}'.format(M.git_username[i])] = len(results)
    return jsonify({'total commit count in 2018':git_commit_count})


############################################################################################
"""2.Total number of commit contributions as above, but restricted to projects that are 
members of the original submitted set."""
############################################################################################
@app.route('/rank2',methods=['GET'])
def ranking2():
    git_commit_count = {}
    for j in range(0,len(M.git_username)):
        link = requests.get("https://api.github.com/repos/"+M.git_username[j]+"/"+M.git_repo[j]+"/commits?since=2018-01-01", auth=(Username, Password))
        data = json.loads(link.text)
        git_commit_count['{0}'.format(M.git_username[j])] = len(data)
    return jsonify({'total commit count in 2018 for the submitted repos':git_commit_count})


############################################################################################
""" 3.The number of known programming languages for each user (presuming that the languages of
any repository committed to are known to the user) """
############################################################################################   
@app.route('/rank3',methods=['GET'])
def ranking3():
    git_language = {}
    for j in range(0,len(M.git_username)):
        link = requests.get("https://api.github.com/users/"+M.git_username[j]+"/repos", auth=(Username, Password))
        json_data = json.loads(link.text)
        results = nested_lookup(key = 'full_name', document = json_data, wild = True, with_keys = False)
      
        new = []
        for l in range(0,len(results)):
            link = requests.get("https://api.github.com/repos/"+results[l]+"/languages", auth=('vimanyuK', 'Pixel2018*('))
            language_data = json.loads(link.text)
            for x in range(0,len(language_data)):
                new.append(list(language_data)[x])

            git_language['{0}'.format(M.git_username[j])] = list(set(new))
    return jsonify({'Known programming languages for each user':git_language})
            


############################################################################################
""" 4.The weekly commit rate of users (provide a weekly rank ordering) for the submitted project set, 
for 2018."""
############################################################################################   
@app.route('/rank4',methods=['GET'])
def ranking4():
    git_commit_rate = {}
    for j in range(0,len(M.git_username)):
        link = requests.get("https://api.github.com/repos/"+M.git_username[j]+"/"+M.git_repo[j]+"/stats/commit_activity", auth=(Username, Password))
        json_data = json.loads(link.text)
        counter = []        
        for i in json_data:
            if ( i['total'] != 0 and ('2018' in (datetime.datetime.fromtimestamp(int(i['week'])).strftime('%Y-%m-%d %H:%M:%S'))) ):

                counter.extend([datetime.datetime.fromtimestamp(int(i['week'])).strftime('%Y-%m-%d %H:%M:%S'), i['total']])
            else:
                continue        
        git_commit_rate['{0}'.format(M.git_username[j])] = counter
    return jsonify({'weekly comits for the year 2018 for the submitted reop':git_commit_rate})
            

############################################################################################
"""  5. The average commit rate of each user to any project, for 2018."""
############################################################################################           
@app.route('/rank5',methods=['GET'])
def ranking5():
    avg_commits = {}
    for k in M.git_username:
        counter = 0
        commits = 0
        link = requests.get("https://api.github.com/users/"+k+"/repos?per_page=100", auth=(Username, Password))
        json_data = json.loads(link.text)
        results = nested_lookup(key = 'name', document = json_data, wild = False, with_keys = False)
        
        for r in results:
            link = requests.get("https://api.github.com/repos/"+k+"/"+r+"/commits?since=2018-01-01", auth=(Username, Password))
            json_data = json.loads(link.text)
            if (len(json_data) != 0):
                counter += 1
                commits = len(json_data) + commits
            else:
                continue
        
        avg_commits['{0}'.format(k)] = (commits/counter)
    
    return jsonify({'The average commit rate of each user to any project, for 2018':avg_commits})


############################################################################################
""" 6. The total number of collaborators in 2018 (ie. a count of other users who have 
contributed to any project that the user has contributed to)."""
############################################################################################         
@app.route('/rank6',methods=['GET'])
def ranking6():
    contributors = {}
    for k in M.git_username:
        count = 0
        offset = 0
        link = requests.get("https://api.github.com/users/"+k+"/repos?per_page=100", auth=(Username,Password))
        json_data = json.loads(link.text)
        results = nested_lookup(key = 'name', document = json_data, wild = False, with_keys = False)
    
        for r in results:
            link = requests.get("https://api.github.com/repos/"+k+"/"+r+"/commits?since=2018-01-01", auth=(Username, Password))
            ddata = json.loads(link.text)
            if (len(ddata) != 0):
                offset = offset + 1
                link = requests.get("https://api.github.com/repos/"+k+"/"+r+"/contributors", auth=(Username,Password))
                data = json.loads(link.text)
                count = count + len(data)
            else:
                continue
        contributors['{0}'.format(k)] = (count - offset)
    return jsonify({'The total number of contributors, for 2018':contributors})


if __name__ == "__main__":
    M = main()
    app.run(port=8080)
    