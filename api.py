# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 12:20:59 2015

@author: lliu5
"""
from get_data_breast import checkAllcancer,get_section
from flask import Flask,request,render_template
from flask_restful import Resource,Api,reqparse
import json
import traceback
app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return render_template('home.html')
    
@app.route('/note',methods=['GET', 'POST'])
def Extract():
    #print request.form
    args = parser.parse_args()
    note = args['data']
    if note == None:
        note = request.form.get('data')
    if note == None:
        return 'No info'
    else:
        result = {}
        try:
            result = checkAllcancer(note)
            result['specimens']=get_section(note)
        except Exception, err:
            print '*'*80
            print err
            print traceback.format_exc()
        return json.dumps(result)
    print '*'*80,'note','['+str(note)+']'
    if request.method == 'POST':
        return 'post method received'
            
    return 'extraction in progress'    
parser =reqparse.RequestParser()
parser.add_argument('data')

if __name__=='__main__':
    app.run(debug=True)