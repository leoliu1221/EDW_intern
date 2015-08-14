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
from confidence_value import getScore
from confidence import keydb_marginal_load,keydb_marginal_newkey,keydb_clean
app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return render_template('home.html')
@app.route('/confidence')
def confidence():
    return render_template('confidence.html')
@app.route('/conf_result',methods=['GET','POST'])
def conf_result():
    args = parser.parse_args()
    key = args['key'] 
    value = args['value']
    cancername = args['cancer']
    marginaldbname = str(cancername)+'.data'
    if key == None:
        key = request.form.get('key')
        value = request.form.get('value')
        cancername = request.form.get('cancername')
        marginaldbname = str(cancername)+'.data'
    if key==None or value == None:
        
        return ' '.join([str(item) for item in ['No info', 'key',key,'value',value,'cancername',cancername]])
    else:

        marginaldb = keydb_marginal_load(marginaldbname)
        keyresult = keydb_marginal_newkey(key,marginaldb)
        valresult = getScore(key,value,keydb_marginal_load('Valdb.data'))
        stringValResult = ' '.join([str(item) for item in value_score.values()])
        return json.dmps([keyresult,stringValResult])

###################################################
### for command line access, namely using the args parse, 
### example commands: curl localhost:5000/cleaner_result -d 'key=your interns are  dumb ' -X POST
### you need to replace the localhost:5000 to the actual website though. 
### in ruby, use Net:HTTP
###example: 
### response = http.post('localhost:5000/cleaner_result','key=interns are dumb')
### responce will be something from response. 
'''
### not that the below code has been tested and it ran succesfully. 
### it should run for all cases as well. 

require 'net/http'

require 'rubygems'
require 'json'
@host = 'localhost'
@port = '5000'
@port_address = 'cleaner_result'

@content = {
"key" => "your interns are dumb"
}.to_json


def post
    req = Net::HTTP::Post.new(@port_address,initheader = {'Content-Type' => 'application/json'})
    req.body = @content
    response = Net::HTTP.new(@host,@port).start {|http| http.request(req)}
    puts "Response #{response.code} #{response.message}: #{response.body}"
    return response.body
    end
thepost = post
puts thepost
'''



###################################################
@app.route('/cleaner_result',methods=['GET','POST'])
def cleaner_result():
    args = parser.parse_args()
    key = args['key']
    if key == None:
        key = request.form.get('key')
    if key == None:
        return 'No info'
    else:
        result = keydb_clean(key)
    return json.dumps(result)


@app.route('/cleaner')
def cleaner():
    return render_template('cleaner.html')

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
                ########################################
                # the below code is for getting confidence score. 
                #########################################                
                for k,v in result[cancer].items():
                    #note that v is a list contains value and original value. 
                    value = v[0]
                    #now we can do value processing. 
                    #put your code here
                    
                    #now we can do key confidence processing. 
                    #it needs a library indicating which unverse it belongs to. 
                    #in here we will just try to use our pre-existing libraries. 
                    #namely, if you have breast cancer as cancer, then
                    try:
                        result_confidence[cancer][k].append(keydb_marginal_newkey(k,marginaldb))
                    except Exception, err:
                        print 'ERROR: key_confidence failed'
                        print err
                    try:
                        value_score = getScore(k,value,keydb_marginal_load('Valdb.data'))
                        result_confidence[cancer][k].append(' '.join([str(item) for item in value_score.values()]))
                    except Exception, err:
                        print 'ERROR: value_confidence failed'
                        print err

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
parser.add_argument('key')
parser.add_argument('value')

if __name__=='__main__':
    app.run(debug=True)
