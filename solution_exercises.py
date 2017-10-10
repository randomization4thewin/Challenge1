from lxml import etree as et #faster
#import xml.etree.ElementTree as et
import numpy as np
import re
import time
import pandas as pd #for printing nicely the output
#%% Query analysis
def string_to_pattern(q):
    # we assume the format: str1 [I1,J1] str2 [I2,J2] str3 ...
    if isinstance(q,str):
        q = q.split()
    
    nWords = np.ceil(len(q)/2)
    words = [q[2* i] for i in range(int(nWords))]
    nums = [re.findall(r'\d+',q[2* i+1]) for i in range(int(nWords-1))]
    I = []; J = []
    for i in range(int(nWords)-1):
        I.append(int(nums[i][0]))
        J.append(int(nums[i][1]))

    pat1 = r'(?=(' + words[0]
    for i in range(1,int(nWords)):
        pat1 = pat1 + '[\s\S]{'+str(I[i-1])+','+str(J[i-1])+'}'+words[i]

    pat1 = pat1 + '))'
    
    return([pat1])

def do_query_nested(s,pat):
    # finds the nested structures using regular expressions
    results = []
    matches = re.finditer(pat, s)
    for match in matches:
        s2 = match.group(1)
        results.append(s2)

        match2 = re.search(pat,s2[:-1])
        while match2:
            results.append(match2.group(1))
            s2 = match2.group(1)
            match2 = re.search(pat,s2[:-1])
    
    return(results)
#%% Paths and queries
path = 'enwiki-20170820-pages-articles-multistream-resized.xml'
Q_testing = ['cats [0,10] are [0,10] to','or [0,10] or [0,10] or','when [15,25] republic [15,25] along']
Qex1 = ['cat [0,10] are [0,10] to','cat [0,100] anatomy','china [30,150] washington','english [0,200] cat','kitten [15,85] cat [0,100] sire [0,200] oxford']
Qex2 = ['arnold [0,10] schwarzenegger [0,10] is','apache [0,100] software','aarhus [30,150] denmark', 'english [0,100] alphabet','first [0,85] letter [0,100] alphabet [0,200] consonant']
Qex3 = ['elephants [0,20] are [0,20] to','technical [0,20] university [0,20] denmark','testing [0,20] with [0,20] a [0,30] lot [0,4] of [0,5] words','stress [0,250] test', 'object [10,200] application [0,100] python [10,200] system [0,100] computer [0,10] science [0,150] linux [0,200] ruby']
#%% Exercise 1 - Cat article
start_time = time.time()
for k in range(5):
    parser = et.iterparse(path)
    test = False
    title = ""
    title_query=[]
    id_article=""
    for event,elem in parser:
        if 'title' == elem.tag:
                if "Cat" == elem.text:
                    title = elem.text
                    test = True
            
        if test:
            if 'text' == elem.tag:
                if event == "end":
                    break
        else:
            elem.clear()
    query_final=do_query_nested(elem.text,string_to_pattern(Qex1[k])[0])
    title_query.append({'title':title,'match':query_final,'id':id_article})
    print(len(title_query),sum(len(title_query[i]['match']) for i in range(len(title_query))))
    # print the result as a data frame - nicer
    df=pd.DataFrame()
    for i in range(len(title_query)):
        df=pd.concat([df,pd.DataFrame({'Article': [title_query[i]['title']]*len(title_query[i]['match']),'Match':title_query[i]['match']})])
    df.to_csv('exercise1_q'+str(k)+'.txt', sep='\t', encoding='utf-8')
print("--- %s seconds ---" % (time.time() - start_time)) 
#1 10
#1 11
#1 1
#1 39
#1 2
# --- around 0.51 seconds per run ---
#There are 5 runs in this loop
#%% Exercise 2 - All articles starting with A or a
start_time = time.time()
for k in range(5):
    parser = et.iterparse(path)
    title = ""
    title_query=[]
    test = False
    for event,elem in parser:
        if 'title' == elem.tag:
            text_test=elem.text[0]
            if "a" == text_test.lower():
                title = elem.text
                test = True
        if test:
            if 'text' == elem.tag:
                    query_final=do_query_nested(elem.text,string_to_pattern(Qex2[k])[0])
                    test=False
                    if query_final:
                        title_query.append({'title':title,'match':query_final})
                        
        else:
            elem.clear()
    print(len(title_query),sum(len(title_query[i]['match']) for i in range(len(title_query))))
    # print the result as a data frame - nicer
    df=pd.DataFrame()
    for i in range(len(title_query)):
        df=pd.concat([df,pd.DataFrame({'Article': [title_query[i]['title']]*len(title_query[i]['match']),'Match':title_query[i]['match']})])
    df.to_csv('exercise2_q'+str(k)+'.txt', sep='\t', encoding='utf-8')
print("--- %s seconds ---" % (time.time() - start_time))
#5 14
#188 1624
#132 564
#97 188
#3 3
# --- around 365.13 seconds per run ---
#There are 5 runs in this loop
#%% Exercise 3 - All articles
start_time = time.time()
for k in range(5):
    parser = et.iterparse(path)
    title = ""
    title_query=[]
    test = False
    for event,elem in parser:
        if 'title' == elem.tag:
            title = elem.text
            test = True
        if test:
            if 'text' == elem.tag:
                    query_final=do_query_nested(elem.text,string_to_pattern(Qex3[k])[0])
                    test=False
                    if query_final:
                        title_query.append({'title':title,'match':query_final})
                        
        else:
            elem.clear()
    print(len(title_query),sum(len(title_query[i]['match']) for i in range(len(title_query))))
    # print the result as a data frame - nicer
    df=pd.DataFrame()
    for i in range(len(title_query)):
        df=pd.concat([df,pd.DataFrame({'Article': [title_query[i]['title']]*len(title_query[i]['match']),'Match':title_query[i]['match']})])
    df.to_csv('exercise3_q'+str(k)+'.txt', sep='\t', encoding='utf-8')
print("--- %s seconds ---" % (time.time() - start_time))
#127 183
#408 611
#0 0
#3494 7570
#1 1
# --- around 1000.24 seconds per run ---
#There are 5 runs in this loop
