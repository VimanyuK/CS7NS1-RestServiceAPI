#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 23:04:35 2018

@author: vimanyu
"""

from flask import Flask, jsonify, abort, render_template, request
from flask_restful import Resource
import requests, json, subprocess, datetime
from nested_lookup import nested_lookup

import smtplib
from smtplib import SMTPException

import os
path = '/home/vimanyu/Documents/flask'
os.chdir(path)
app = Flask(__name__)


"""Github account username and password to use the api for testing purposes, can not ping more than the set limit without credentials."""

Username = "cs7ns1"
Password = "Datascience2018*("

class main():
    def __init__(self):
        self.number_of_users = int(input ('Enter the number username/repos you want to enter:'))
        self.git_username = []
        self.git_repo = []
        self.git_users = {}
        self.git_mail = {}

        while(self.number_of_users != 0):
            self.user_name = input('Enter the user name: ')
            self.git_username.append(self.user_name)
            self.repo_name = input('Enter the repository name: ')
            self.git_repo.append(self.repo_name)
            self.number_of_users = self.number_of_users-1
        self.git_users = dict(zip(self.git_username,self.git_repo))


@app.route("/")
def GitUsers():
    return render_template("welcome.html", dat = M.git_users)


@app.route('/to_add')
def GittoAdd():
    return render_template("to_add.html")

@app.route('/add', methods = ['POST','GET'])
def GitAdd():
    if request.method == 'POST':
        result = request.form
        key = request.form.getlist('UserName')
        value = request.form.getlist('RepoName')
        M.git_users.update({key[0]:value[0]})
        M.git_username.append(key[0])
        M.git_repo.append(value[0])
    return render_template("add.html",result = result)


@app.route('/to_delete')
def GittoDelete():
    return render_template("to_delete.html")

@app.route('/delete', methods = ['POST','GET'])
def GitDelete():
    if request.method == 'POST':
        result = request.form
        key = request.form.getlist('UserName')
        del M.git_users[key[0]]
        ind = M.git_username.index(key[0])
        del M.git_repo[ind]
        M.git_username.remove(key[0])
    return render_template("delete.html",result = result)


@app.route('/to_update')
def GittoUpdate():
    return render_template("to_update.html")

@app.route('/update', methods = ['POST','GET'])
def GitUpdate():
    if request.method == 'POST':
        result = request.form
        key = request.form.getlist('UserName')
        value = request.form.getlist('RepoName')
        for x in M.git_users:
            if x == key[0]:
                M.git_users.update({key[0]:value[0]})
                M.git_username.append(key[0])
                M.git_repo.append(value[0])
    return render_template("update.html",result = result)


@app.route('/rank1')
def GitRank1():
    git_commit_count = {}
    for i in range(0,len(M.git_username)):
        git_user_data = {}
        temp = subprocess.check_output(["curl", "-H", "Accept: application/vnd.github.cloak-preview", "https://api.github.com/search/commits?q=author:"+M.git_username[i]+"&per_page=100"],shell=False).decode('utf-8')
        git_user_data['{0}'.format(M.git_username[i])] = json.loads(temp)
        results = nested_lookup(key = 'date', document = git_user_data, wild = True, with_keys = False)
        results = list(set(results))
        results = [x for x in results if ("2018" in x)]
        git_commit_count['{0}'.format(M.git_username[i])] = len(results)

    od = dict(sorted(git_commit_count.items(),key = lambda x:x[1], reverse=True))
    M.git_mail.update(od)
    return render_template("rank1.html", result = od)


@app.route('/rank2')
def GitRank2():
    git_commit_count2 = {}
    for j in range(0,len(M.git_username)):
        link = requests.get("https://api.github.com/repos/"+M.git_username[j]+"/"+M.git_repo[j]+"/commits?since=2018-01-01", auth=(Username, Password))
        data = json.loads(link.text)
        user_repo = M.git_username[j]+'/'+M.git_repo[j]
        git_commit_count2['{0}'.format(user_repo)] = len(data)

    od = dict(sorted(git_commit_count2.items(),key = lambda x:x[1], reverse=True))
    M.git_mail.update(od)
    return render_template("rank2.html", result = od )


@app.route('/rank3')
def GitRank3():
    git_language = {}
    for j in range(0,len(M.git_username)):
        link = requests.get("https://api.github.com/users/"+M.git_username[j]+"/repos", auth=(Username, Password))
        json_data = json.loads(link.text)
        results = nested_lookup(key = 'full_name', document = json_data, wild = True, with_keys = False)

        lang_count = {}
        new = []
        for l in range(0,len(results)):
            link = requests.get("https://api.github.com/repos/"+results[l]+"/languages", auth=(Username, Password))
            language_data = json.loads(link.text)
            for x in range(0,len(language_data)):
                new.append(list(language_data)[x])
            git_language['{0}'.format(M.git_username[j])] = list(set(new))

    od = dict(sorted(git_language.items(),key = lambda x:len(x[1]), reverse=True))
    M.git_mail.update(od)
    return render_template("rank3.html", result = od )


@app.route('/rank4')
def GitRank4():
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
        user_repo = M.git_username[j]+'/'+M.git_repo[j]
        git_commit_rate['{0}'.format(user_repo)] = counter
    od = dict(sorted(git_commit_rate.items(),key = lambda x:len(x[1]), reverse=True))
    
    return render_template("rank4.html", result = od )


@app.route('/rank5')
def GitRank5():
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
    od = dict(sorted(avg_commits.items(),key = lambda x:x[1], reverse=True))
    M.git_mail.update(od)
    return render_template("rank5.html", result = od)


@app.route('/rank6')
def GitRank6():
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

    od = dict(sorted(contributors.items(),key = lambda x:x[1], reverse=True))
    M.git_mail.update(od)
    return render_template("rank6.html", result = od)


@app.route('/to_mail')
def Gittomail():
    return render_template("to_mail.html")

@app.route('/mail', methods = ['POST','GET'])
def Gitmail():
    if request.method == 'POST':
        result = request.form
        sender = request.form.getlist('fromemailID')
        password = request.form.getlist('password')
        reciever = request.form.getlist('toemailId')

        msg = "\n"+str(M.git_mail)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        while True:
            try:
                server.login(sender[0], password[0])
            except:
                print("Error: Bad credentials")
                result = "Error: Bad credentials"
                break
            try:
                server.sendmail(sender[0], reciever[0], msg)
                print('Mail sent')
                result = "Mail sent"
                break
            except SMTPException:
                print ("Error: unable to send email")
                result = "Error: unable to send email"
                break

    return render_template("mail.html", result = result)

if __name__ == "__main__":
    M = main()
    app.run(port =8080)

#YuzhouPeng/CS7IS5-Adaptive-Application
#vimanyuk/DataVis_InteractiveBubbleChart
#hanutm/Visualization
#ShrubinS/swim-protocol
