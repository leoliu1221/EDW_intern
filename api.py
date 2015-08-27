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

@app.route("/jsontest",methods=['GET','POST'])
def jsontest():
    '''
    parser.add_argument('text')
    parser.add_argument('key')
    parser.add_argument('about_type')
    parser.add_argument('value')
    parser.add_argument('universe_id')
    parser.add_argument('suggestions_uri')
    parser.add_argument('universe_name')
    parser.add_argument('universe_name_variants')
        
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
    if note is None:
        note= '"A.\tRIGHT BREAST, NEEDLE LOCALIZED LUMPECTOMY:\n-\tINFILTRATING DUCTAL CARCINOMA, GRADE 3 OF 3, MEASURING 1.7 CM IN GREATEST DIMENSION.\n-\tDUCTAL CARCINOMA IN SITU (DCIS), SOLID AND COMEDO-TYPES, NUCLEAR GRADE 3, WITH MICROCALCIFICATIONS:\n-\tLYMPHOVASCULAR INVASION IDENTIFIED.\n-\tINVASIVE CARCINOMA AND DCIS ARE PRESENT WITHIN LESS THAN 0.1 CM OF THE SUPERIOR MARGIN ON THE MAIN SPECIMEN (SEE PARTS B-G FOR FINAL STATUS OF MARGINS).\n-\tBIOPSY SITE CHANGES.\n-\tREMAINING BREAST TISSUE WITH USUAL DUCTAL HYPERPLASIA, APOCRINE METAPLASIA, AND SCLEROSING ADENOSIS WITH MICROCALCIFICATIONS.\n\nB.\tRIGHT BREAST, ANTERIOR SUBAREOLAR MARGIN, EXCISION:\n-\tBREAST TISSUE, NO TUMOR IDENTIFIED.\n\nC.\tRIGHT BREAST, LATERAL MARGIN, EXCISION:\n-\tBREAST TISSUE, NO TUMOR IDENTIFIED.\n\nD.\tRIGHT BREAST, MEDIAL MARGIN, EXCISION:\n-\tBREAST TISSUE, NO TUMOR IDENTIFIED.\n\nE.\tRIGHT BREAST, DEEP MARGIN, EXCISION:\n-\tMINUTE FOCUS OF INFILTRATING DUCTAL CARCINOMA, GRADE 3 OF 3, MEASURING LESS THAN 0.1 CM IN GREATEST DIMENSION.\n-\tFINAL MARGIN NEGATIVE FOR TUMOR (0.6 CM FROM TUMOR).\n\nF.\tRIGHT BREAST, INFERIOR MARGIN, EXCISION:\n-\tBREAST TISSUE, NO TUMOR IDENTIFIED.\n\nG.\tRIGHT BREAST, SUPERIOR MARGIN, EXCISION:\n-\tBREAST TISSUE, NO TUMOR IDENTIFIED.\n\nH.\tLYMPH NODES, RIGHT AXILLARY SENTINEL, EXCISION:\n-\tTWO LYMPH NODES, NEGATIVE FOR METASTATIC CARCINOMA (0/2).\n\n\n Invasive Breast Cancer Staging Summary \t\nSpecimen Submitted:\tRight breast needle localized lumpectomy\t\nSpecimen Dimensions:\t4.1 x 3.9 x 1.8 cm\t\nTumor Size:\t1.7 cm\t\n \t(Based on the most representative gross or microscopic measurement of the invasive component only)\t\t\nHistologic Type:\tDuctal\t\nGrade:\t3\t\nLymphatic Vascular Invasion:\tPresent\t\nDCIS as Extensive Intraductal Component:\tAbsent\t\n\tDCIS Measurement/Proportion:\t10%\t\nLCIS:\tAbsent\t\nCalcifications:\tPresent\t\n\tLocations of Calcifications:\tBenign and malignant tissue\t\nMargins of Excision:\t\n\tInvasive Cancer:\tNegative\t\n\tDistance to Margin:\t0.6 cm to deep margin\t\n\tDCIS:\tNegative\t\n\tDistance to Margin:\tWidely free\t\nAxillary Lymph Nodes:\t\t\n\tNumber of Positive Versus Total:\t0/2\t\n\tSize of Largest Metastasis:\tN/A\t\n\tExtranodal Extension:\tN/A\t\nBreast Tumor Markers:\t(Per S-12-14475)\t\n\tER:\tLow Positive; 5%\t\n\tPR:\tLow Positive; 5%\t\n\tHER2:\tNegative; 1+\t\n\tKi-67\tHigh (Unfavorable); 30%\t\n\tp53:\tNegative; 0%\t\nTumor Bank:\tNo\t\nTNM Staging:\tpT1c-N0(SN)-MX\t\nGrading of invasive carcinoma is based on the modified Bloom-Richardson system as described in Protocol for the Examination of Specimens from Patients with Invasive Carcinoma of the Breast, a publication of the College of American Pathologists (CAP), updated on 2009.  The TNM staging is based on the recommendations of the American Joint Commission on Cancer (AJCC, 7th Edition, 2010).\t\n"""\n'

    #process the note since we have cleared everything else. 
    if note is not None:
        result_all = check_all_cancer(note)
        result = []
        for key in result_all.keys():
            if  in_variants(key,universe_name_variants):
                temp = {}
                temp['galaxy'] = result_all[key]                
                result.append(temp)
        #filter out the cancer types listed.
        end = post_json(universe_id,about_type,about_id,result,uri=suggestions_uri)
        return end
        #todo: process the notes. 
        #s2 = 'TUMOR TYPE:\t\t\t\t\t\t\tENDOMETRIOID ADENOCARCINOMA\n\tSIZE:\t\t\t\t\t\t\t\t0.5 CM THICKNESS\n\tFIGO GRADE\t\t\t\t\t\t\n\t\tOVERALL:\t\t\t\t\t\t1\n\t\tARCHITECTURAL:\t\t\t\tGLANDULAR\n\t\tNUCLEAR:\t\t\t\t\t\tLOW-GRADE\t'   
        #test = Datapoint(s2) 
        #result = [test,test,test]        
        
###################################################
@app.route('/cleaner_result',methods=['GET','POST'])
def cleaner_result():
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
    parser.add_argument('text')
    parser.add_argument('key')
    parser.add_argument('about_type')
    parser.add_argument('value')
    parser.add_argument('universe_id')
    parser.add_argument('suggestions_uri')
    parser.add_argument('universe_name')
    parser.add_argument('universe_name_variants')
        
    '''
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
