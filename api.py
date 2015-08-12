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
from confidence import keydb_marginal_load
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
            result_confidence= result.copy()
            for cancer in result.keys():
                marginaldbname = cancer.split()[0].lower()+'.data'
                print 'marginaldbname: ',marginaldbname
                marginaldb = keydb_marginal_load(marginaldbname)
                for k,v in result[cancer].items():
                    #note that v is a list contains value and original value. 
                    value = v[0]
                    #now we can do value processing. 
                    
                    #now we can do key confidence processing. 
                    #it needs a library indicating which unverse it belongs to. 
                    #in here we will just try to use our pre-existing libraries. 
                    #namely, if you have breast cancer as cancer, then
                    #your splited cancer will have the name as the first value. 
                    
                    result_confidence[cancer][k].append(keydb_marginal_newkey(value,marginaldb))
            
            result['specimens']=get_section(note)
        except Exception, err:
            print '*'*80
            print err
            print traceback.format_exc()
        return json.dumps(result,result_confidence)
    print '*'*80,'note','['+str(note)+']'
    if request.method == 'POST':
        return 'post method received'
            
    return 'extraction in progress'    
parser =reqparse.RequestParser()
parser.add_argument('data')

if __name__=='__main__':
    app.run(debug=True)
