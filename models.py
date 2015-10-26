from jsonweb.encode import to_object, dumper
from confidence import keydb_marginal_newkey
from confidence_value import getScore
from jsonweb import decode, encode
import re
@encode.to_object()
class Datapoint:
    
    #constrctor 
    def __init__(self,message=None,marginaldb = None,valdb = None):
        if message is None:
            self.key = ''
            self.value = ''
            self.sub_keys = []
            self.origin = ''
            self.key_score = ''
            self.value_score = ''
        else:
            if message=='':
                self.key=''
                self.value=''
                self.sub_keys=[]
                self.origin = ''
            #take the first line as key-value, and then pass the rest to find subs. 
            lines = message.split('\n')
            #replace ......> into :
            pattern = re.compile(r'([^\.^\:]+):*[\.]*>+([^\.]+)')
            match = pattern.match(lines[0])
            if match:
                lines[0] = match.group(1)+':'+match.group(2)
            if ':' not in lines[0]:          
                lines[0] = lines[0].replace('\t',':',1)
            line0 = lines[0].strip().split(':')
#            print 'line0',line0
            self.key = line0[0].strip()
            if len(line0)>1:
                self.value = line0[1].strip()
            else:
                self.value=''
            self.origin = lines[0]
            if len(lines)>1:
                self.sub_keys = self.find_subs(message.split('\n')[1:])
            else:
                self.sub_keys = []
            self.key_score = ''
            self.value_score = ''
            try:
                self.set_key_score(marginaldb = marginaldb)
                self.set_value_score(valdb = valdb)
            except Exception, err:
                print err
                print 'ERROR: not able to get key score or value score.'
                print 'score for',self.key,self.value,'is not calculated'
    def set_key_score(self,marginaldb):
        self.key_score = keydb_marginal_newkey(self.key,marginaldb = marginaldb,dbName = None,add=False)
    def set_value_score(self,valdb):
#        print "key",self.key,"value",self.value
        self.value_score = getScore(self.key,self.value,valdb = valdb, add=True)
        

    def find_subs(self,lineList):
#        print 'in find_subs'
        #reduce the level by \t. 
        #if the line does not have \t then print.
        lines = []
        for line in lineList:
#            print 'line is:',line
            if len(line)>2 and line[0]==' ' and line[1].isalpha():
                line = line.replace(' ','\t')
            if not line.startswith('\t'):
                pass
#                print 'did not process line:',line
            else:
                if line.strip()=='':
                    continue
                else:
                    lines.append(line.replace('\t','',1))
        result = []
        curr = None
        for item in lines:
            if curr is None:
                curr = item+'\n'
            elif not item.startswith('\t'):
                result.append(curr)
                curr = item+'\n'
            else:
                #now deal with all those that has '\t' in front:
                curr= curr + item+'\n'
        #now result has all strings that can be turned into Datapoint
        if curr is not None and curr.strip()!='': result.append(curr)
        return [Datapoint(s) for s in result]
        
    def __repr__(self):
            return '<Datapoint : '+self.key+'>'
    def __str__(self):
            return self.key+':'+self.value
