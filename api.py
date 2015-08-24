# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 12:20:59 2015

@author: lliu5
"""
from models import Datapoint, dumper
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
    from confidence import keydb_get_dbs
    files = keydb_get_dbs()
    return render_template('home.html',files = files)
@app.route('/confidence')
def confidence():
    return render_template('confidence.html')
@app.route('/conf_result',methods=['GET','POST'])
def conf_result():
    args = parser.parse_args()
    key = args['key'] 
    value = args['value']
    cancername = args['cancer']
    if cancername.strip()=='':
        cancername  = args.get('cancer_select')
    if cancername == None:
        cancername = request.form.get('cancer_select')
        
    marginaldbname = str(cancername)+'.data'
    if key == None:
        key = request.form.get('key')
        value = request.form.get('value')
        cancername = request.form.get('cancername')
        if cancername==None:
            cancername  = request.form.get('cancer_select')
        marginaldbname = str(cancername)+'.data'
    if key==None or value == None:
        
        return ' '.join([str(item) for item in ['No info', 'key',key,'value',value,'cancername',cancername]])
    else:
        keyresult = ''
        try:
            marginaldb = keydb_marginal_load(marginaldbname)
            keyresult = keydb_marginal_newkey(key,marginaldb)
        except Exception,err:
            print err
            print 'ERROR: key db error'
        
        stringValResult = ''
        try:
            valresult = getScore(key,value,keydb_marginal_load('Valdb.data'))
            stringValResult = ' '.join([str(item) for item in valresult.values()])
        except Exception, err:
            print err
            print 'ERROR: val db error'
        return json.dumps([keyresult,stringValResult])

###################################################
### for command line access, namely using the args parse, 
### example commands: curl localhost:5000/cleaner_result -d 'key=your interns are  dumb ' -X POST
### you need to replace the localhost:5000 to the actual website though. 
### in ruby, use Net:HTTP
###example: 
### response = http.post('localhost:5000/cleaner_result','key=interns are dumb')
### responce will be something from response. 
'''
######################################
######################################
#TODO:
# making cancer into a code. 
# universe_id, text, about_type, about_id,suggestions_uri,universe_name, universe_name_variants(array)
# sending back POST: universe_id = integer, about_type = string, about_id = integer, result = hash
hash: 
[
    {
        'key':key1, 
        'value': value1,
        'origin':original_key_value,
        'key_score':key_score,
        'value_score':value_score
        'sub_keys': 
        [
            {
            'key':subkey1
            'value':subvalue1
            'origin':suborigin1
            'key_score':subkey_score
            'value_score':subvalue_score
            'sub_keys': []            
            }
        ]
    }
]

...
}
# transform subkey into primarykey - subkey - value system (subkey can be another primary key for other subkeys as well)
# clean values and keys after getting results. 

### note that the below code has been tested and it ran succesfully. 
### it should run for all cases as well. 

require 'net/http'

require 'rubygems'
require 'json'
@host = 'localhost'
@port = '5000'
@port_address = 'cleaner_result'

@content = {
"data" => "your interns are dumb",
"cancer" => "thyroid"
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

@app.route("/jsontest")
def jsontest():
    s2 = 'Breast Tumor Markers: (combined with report of S-12-11788)\t_\t\n\tER:\t>95%, strong positive\t\n\tPR:\t  95%, strong positive\t\n\tHER2:\t     0%, score 0, negative\t\n\tKi-67\t10-15%, intermediate\t\n\tp53:\t     0%, negative\t'
    test = Datapoint(s2)
    test2 = [test,test,test,test]
    return dumper(test2)
###################################################
@app.route('/cleaner_result',methods=['GET','POST'])
def cleaner_result():
    args = parser.parse_args()
    key = args['key']
    print args
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
    note = args['text']
    cancerName = args['universe_id']
    print 'args:',args
    print 'form:',request.form
    #should ahve just check form first then the args. 
    if note == None:
        note = request.form.get('data')
        cancerName = request.form.get('cancer')
        
    if cancerName is None:
        cancerName = ''
        
    if note == None:
        return 'No info'
    else:
        result = {}
        try:
            result = checkAllcancer(note)
            result_confidence= result.copy()
            for cancer in result.keys():
                if cancerName.strip() != '':
                    marginaldbname = cancerName.lower()+'.data'
                else:
                    marginaldbname=None
                print 'marginaldbname: ',marginaldbname
                if marginaldbname is not None:
                    marginaldb = keydb_marginal_load(marginaldbname)
                else:
                    marginaldb = keydb_marginal_load()
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
                        result_confidence[cancer][k].append(keydb_marginal_newkey(k,value,marginaldb,marginaldbname,True))
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
parser.add_argument('text')
parser.add_argument('key')
parser.add_argument('about_type')
parser.add_argument('value')
parser.add_argument('universe_id')
parser.add_argument('suggestions_uri')
parser.add_argument('universe_name')
parser.add_argument('universe_name_variants')

if __name__=='__main__':
    app.run(debug=True)
