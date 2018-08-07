#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 23:04:35 2018

@author: vimanyu
"""

from flask import Flask, render_template, request
import os
path = '/home/vimanyu/Documents/flask'
os.chdir(path)
app = Flask(__name__)


class main():
    def __init__(self):
        self.number_of_users = int(input ('Enter the number username/repos you want to enter:'))
        self.git_username = []
        self.git_repo = []
        self.git_users = {}

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
    return render_template("update.html",result = result)


if __name__ == "__main__":
    M = main()
    app.run(port =8080)
