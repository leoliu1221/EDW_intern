# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 12:20:59 2015

@author: liuliu
"""
from flask import Flask,render_template

import json
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    '''
    Returns: 
        render home.html. 
    '''
    files =[]
    return render_template('home.html',files = files)

@app.route('/houseclean')
def confidence():
    '''
    returns:
        render houseclean.html
    '''
    return render_template('houseclean.html')


@app.route('/anniversary')
def cleaner():
    return render_template('anniversary.html')

if __name__=='__main__':
    from send_txt import email
    email(address='2243100552@messaging.sprintpcs.com',content='this is working right?')
    #app.run(debug=True)
