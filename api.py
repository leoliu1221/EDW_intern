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
from http_utilities import post_json
from extraction_engine import check_all_cancer
from file_utilities import in_variants
app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    '''
    Returns: 
        render home.html. 
    '''
    from confidence import keydb_get_dbs
    files = keydb_get_dbs()
    return render_template('home.html',files = files)
@app.route('/confidence')
def confidence():
    '''
    returns:
        render confidence.html
    '''
    return render_template('confidence.html')
@app.route('/conf_result',methods=['GET','POST'])
def conf_result():
    '''
    deprecated. 
    returns the confidence result. 
    Keyscore and value score. 
    1. get arguments from parser
    2. use arguments to feed into our keydb_marginal_newkey and get_score from confidenceval
    3. return the result in json format. 
    '''
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

@app.route("/jsontest",methods=['GET','POST'])
def jsontest():
    '''
    Main access point. 
    1. get the arguments from parser
    2. give default values to those arguments if not exists
    3. process all arguments, getting key score and value score from inside of datapoint datastrcture.     
    4. post the json result back to the uri specified in suggestions_uri field. if not given, will post back to google.     
    5. Also returns the json result sychronously.     
    #TODO
    future operations require creating a new thread for each post received access.     
        
    '''
    args = parser.parse_args()
    note = args.get('text')
    about_type = args.get('about_type')
    universe_id = args.get('universe_id')
    suggestions_uri = args.get('suggestions_uri')
    universe_name = args.get('universe_name')
    universe_name_variants = args.get('universe_name_variants')
    about_id = args.get('about_id')
    print note,about_type,universe_id,suggestions_uri,universe_name,universe_name_variants
    if suggestions_uri is None:
        suggestions_uri="http://google.com"
    if universe_id is None:
        universe_id = 0
    if about_type is None:
        about_type = 'some type'
    if about_id is None:
        about_id = 0
    if universe_name_variants is None:
        universe_name_variants = ['breast']
    fakenote= u'\nbreast cancer staging summary \ngrade:4\nTNM staging: t:4\n\n'
    if note is None:
        note=fakenote
    note = note.decode('string_escape')
    #process the note since we have cleared everything else. 
    if note is not None:
        result_all = check_all_cancer(note)
        print 'resultall',result_all
	result = []
        for key in result_all.keys():
            if  in_variants(key,universe_name_variants):
                temp = {}
                temp['galaxy'] = result_all[key]                
                result.append(temp)
        #filter out the cancer types listed.
        end = post_json(universe_id,about_type,about_id,result,uri=suggestions_uri)
        return 'Success: Posted to '+suggestions_uri
        #todo: process the notes. 
        #s2 = 'TUMOR TYPE:\t\t\t\t\t\t\tENDOMETRIOID ADENOCARCINOMA\n\tSIZE:\t\t\t\t\t\t\t\t0.5 CM THICKNESS\n\tFIGO GRADE\t\t\t\t\t\t\n\t\tOVERALL:\t\t\t\t\t\t1\n\t\tARCHITECTURAL:\t\t\t\tGLANDULAR\n\t\tNUCLEAR:\t\t\t\t\t\tLOW-GRADE\t'   
        #test = Datapoint(s2) 
        #result = [test,test,test]        
        
###################################################
@app.route('/cleaner_result',methods=['GET','POST'])
def cleaner_result():
    '''
    '''
    args = parser.parse_args()
    key = args['key']
    print args
    if key == None:
        key = request.form.get('key')
    if key == None or key.strip() == '':
        return 'No info'
    else:
        result = keydb_clean(key)
    
    return json.dumps(result)


@app.route('/cleaner')
def cleaner():
    return render_template('cleaner.html')

@app.route('/note',methods=['GET', 'POST'])
def Extract():
    '''
    depracted. Use jsontest instead. 
    this is a nice web interface for testing. 
    user only needs to input text and a univerid, 
    Returns: 
        json formated result from given text and universe_id
    '''
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
        
    if note == None or note.strip()=='':
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
parser.add_argument('about_id')
parser.add_argument('value')
parser.add_argument('universe_id')
parser.add_argument('suggestions_uri')
parser.add_argument('universe_name')
parser.add_argument('universe_name_variants')

if __name__=='__main__':
    app.run(debug=True)
