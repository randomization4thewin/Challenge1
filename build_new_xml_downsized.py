from lxml import etree as et
import time

path = "enwiki-20170820-pages-articles-multistream.xml"
#%% 
parser = et.iterparse(path)
test = False
title = ""
text = ""
ID = ""
counter=0
xmlFile = "enwiki-20170820-pages-articles-multistream-resized.xml"
f = open(xmlFile,'w', encoding='utf-8')
f.write('<?xml version=\'1.0\' encoding=\'utf-8\'?>')
f.write('\n')
f.write('<root>')
start_time = time.time()
written = False

# we assume that all pages have a text and a title field
for event,elem in parser:
    if 'title' == elem.tag[43:]: # extract the title, we are at the beginning of a page
        if isinstance(elem.text, str):
            title = elem.text
            test=True
        else: # we don't save pages without titles
            test = False
    
    if test and 'ns' == elem.tag[43:]:
        if not elem.text == '0': # thens it's not an article
            test = False
    
    if test and 'text' == elem.tag[43:]: # extract text
        text=elem.text
        if isinstance(text, str): # preprocess
            text=" ".join(text.split())
            text=text.lower()
        else: # we don't save pages without any text
            test = False
            
    if test and 'redirect' == elem.tag[43:]: # then this page should be skipped
        test = False
    
    if test and 'id' == elem.tag[43:]: # Extract ID
        ID = elem.text
    
    if test and 'page' == elem.tag[43:]: # we have reached the end of the page
                                         # plus we haven't met a 'redirect' tag
        page = et.Element("page")
        et.SubElement(page,"id").text = ID
        et.SubElement(page, "title").text = title
        et.SubElement(page, "text").text = text
        f.write('\n')
        f.write(et.tounicode(page))
        page.clear()
        
        # Reset values
        title = ""
        text = ""
        ID = ""
        written = True
        test = False
        counter += 1
        
    elem.clear()
        
    if written and counter%10000 == 0: # keep track of proces
        written = False
        print('Iteration %d, elapsed time %.5s seconds ----' % (counter, time.time() - start_time))
        

f.write('\n')
f.write('</root>')
f.close()
print('Iteration %d, elapsed time %.5s seconds ----' % (counter, time.time() - start_time))