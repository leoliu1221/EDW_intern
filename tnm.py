'''
fileName: tnm.py
Usage: mainly for use the function get_stage_from_pa
Wanted to create a parser that checks for all lines in the text
If the line has tnm system then outputs the tnm system staging
'''
def get_tnm(text,confFile = 'stageKeys.yaml'):
    '''
    Check if a pa note has a stage associate with colon cancer
    Args:
        text: a string of input text
    Returns:
        result:
            a dictionary of stage -> line number
    '''
    #text = data[2009670][0][4]
    if text.find('ajcc')==-1 and text.find('tnm')==-1:
        print 'cannot find keyword ajcc or tnm'
        return {}
    import yaml
    with open(confFile,'r') as f:
        cfg = yaml.load(f)
    #loading the stage and keyword from file 'stageKeys.yaml'
    stages = cfg['stages']
    keywords = cfg['keys']

    #1. try to get the ajcc from the text
    lines = text.split('.')
    lineNum=0
    result = {}
    for line in lines:
        textKeys = []
        for key in keywords:
            if key in text:
                textKeys.append(key)
        for stage in stages.keys():
           req = stages[stage].values()
           if meetReq(textKeys,req):
                if result.get(stage) == None:
                    result[stage]=[]
                result[str(stage)].append(lineNum)
        lineNum+=1
    for key in result.keys():
        result[key] = list(set(result[key]))
    return result
