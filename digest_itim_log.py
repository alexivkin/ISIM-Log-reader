#!/usr/bin/python
""" ITIM log digester
2015 (c) Alex Ivkin v1.2

Usage: python digest_itim_log.py <trace.log|msg.log>

Creates a digest in a CSV format for a TIM log file that is more human-readable than the original format.
"""

import re,sys,traceback,os,csv
from xml.dom import minidom
#import copy
#import pp     #Parallel Python, see http://www.parallelpython.com

if len(sys.argv)==1:
    print __doc__
    sys.exit(1)

filepathandname=os.path.splitext(sys.argv[1])[0]
digest={'Name':os.path.basename(filepathandname)}

digestfields="Name,Date,Time,CTGIM,Exception,Log Text,Exception Text".split(",")
fout=csv.DictWriter(open(filepathandname+"_digest.csv",'wb'),digestfields)
fout.writerow(dict((fn,fn) for fn in digestfields)) # write the header = f_services.writeheader() in python 2.7

fin=open(sys.argv[1],'r')
lines=fin.readlines()
message=False
count=0

for line in lines:
    count+=1
    if re.match(r'(<Message|<Trace)',line):
        message=True
        block=""
        percent = int(count*100/len(lines))
        sys.stdout.write("\rProcessing...%d%%" % percent)
        sys.stdout.flush()
    if message:
        block+=re.sub(r'[^\11\12\15\40-\176]','',line) # swallow non-ascii stuff
    if re.match(r'(</Message>|</Trace>)',line):
        message=False
#        print "parsing "+block
        try:
            doc=minidom.parseString(block)
            root=doc.firstChild
            datetime=re.sub('-\d\d:00','',root.getElementsByTagName("Time")[0].firstChild.data.strip())
            digest['Date']=datetime.split()[0]
            digest['Time']=datetime.split()[1][:8] # trim up the time for excel to auto-recognise in a csv
            #source=root.getElementsByTagName("Source")[0].attributes["FileName"].value - not currently used
            ctgim=""
            logtext=""
            exception=""
            errortext=""
            #ctgim=root.getAttribute("Id") # root.attributes["Id"].value also works
            ctgimpattern=re.compile(r'CTGIM\w\d\d\d\w')
            exceptionpattern=re.compile(r'((?P<type1>(\w+\.){2,}\w+):\D)|(?P<type2>(\w+\.){2,}\w+Exception)',re.S) # a very advanced regexp to catch the exception patterns. Uses group names (?<..>) to deal with the | (or) match to ease the floating of the matching group between \1 and \4 or so
            if root.getElementsByTagName("LogText")[0].firstChild is not None:
                lognodes=root.getElementsByTagName("LogText")[0]
                if lognodes.childNodes.length > 1: # this is the case under jython's 2.5 minidom dealing with \n inside CDATA blocks
                    # for some reason multiline text inside of CDATA is not being treated as a single child but multiple
                    #logtext="".join([node.data.strip() for node in lognodes.childNodes]) # jam the text together
                    logtext=lognodes.firstChild.data+str(lognodes.childNodes.item(1).data).strip()  # get only the first two lines
                else:  # this would happen running under python 2.7 minidom
                    #logtext=re.sub('^(.*?\n.*?\n)(.|\n)*',r'\1',lognodes.firstChild.data.strip()) # trim to the first two lines only
                    logtext=" ".join(lognodes.firstChild.data.split()) # compress consequitive spaces and remove new lines
                    #logtext=re.sub(r'\n','',lognodes.firstChild.data.strip())
                logtext=re.sub('The following definition error occurred.\s?Error:','',logtext) # remove redundant junk
            if len(root.getElementsByTagName("Exception")) > 0 and root.getElementsByTagName("Exception")[0].firstChild is not None:
                exceptionnodes=root.getElementsByTagName("Exception")[0]
                if exceptionnodes.childNodes.length > 1: # this is the case under jython's 2.5 minidom dealing with \n inside CDATA blocks
                    errortext=exceptionnodes.firstChild.data+str(exceptionnodes.childNodes.item(1).data).strip() # get only the first two lines
                else: # this would happen running under python 2.7 minidom
                    errortext=re.sub('^(.*?\n.*?\n)(.|\n)*',r'\1',exceptionnodes.firstChild.data.strip()) # trim to the first two lines only
                    errortext=" ".join(errortext.split()) # compress consequitive spaces and remove new lines
            # plop exceptions and ITIM message numbers out
            if ctgimpattern.search(logtext):
                ctgim=ctgimpattern.search(logtext).group(0) # extract the ctgim code from the log text
                logtext=re.sub('\s*'+ctgim+'\s*',' ',logtext).strip() # remove ctgim from the remaining text
            if ctgimpattern.search(errortext):
                ctgim=ctgimpattern.search(errortext).group(0) # extract the ctgim code from the error text
                errortext=re.sub('\s*'+ctgim+'\s*',' ',errortext).strip()
            if exceptionpattern.search(logtext):
                exceptionmatch=exceptionpattern.search(logtext)
                exception=exceptionmatch.group('type1' if exceptionmatch.group('type1') is not None else 'type2')
                logtext=re.sub('\s*'+exception+':?\s*',' ',logtext).strip()
            if exceptionpattern.search(errortext):
                exceptionmatch=exceptionpattern.search(errortext)
                exception=exceptionmatch.group('type1' if exceptionmatch.group('type1') is not None else 'type2')
                errortext=re.sub('\s*'+exception+':?\s*',' ',errortext).strip()
            #fout.write('%s,%s,%s,%s,%s,"%s","%s"\n' % (filenameonly,date,time,ctgim,exception,logtext,errortext))
            digest['CTGIM']=ctgim
            digest['Exception']=exception
            digest['Log Text']=logtext
            digest['Exception Text']=errortext
            fout.writerow(digest)
        except:
            #print doc.toxml()
            print block[:200]+"...\n"
            #print " ".join([str(element) for element in sys.exc_info()[:2]])
            traceback.print_exc()
            sys.exit(1)
sys.stdout.write("\rProcessing...%d%%" % 100) # eye candy
sys.stdout.flush()

# dumb plain text parser. for reference only
def lineparser(lines):
    outline=""
    for line in lines:
        #print line
        line=line.strip()
        try:
            if message:
                outline+=line
            if re.search("<Time",line):
                outline+=re.search(r'>(.*)<',line).group(0)[2:-1]+' '
            if re.search("<Exception",line):
                outline+="EXC:"+re.search(r'CDATA\[(.*)',line).group(0)[6:]
            if re.search("<LogText",line):
                message=True
                outline+=re.search(r'CDATA\[(.*)',line).group(0)[6:]
            if re.search('\]\]',line):
                message=False
                outline+=re.search(r'(.*)\]\]',line).group(0)[:-2]
                #print outline
            if re.match(r'(<Message|<Trace)',line):
                outline=""
            if re.match(r'(</Message>|</Trace>)',line):
                fout.write(outline+'\n')

            print outline
        #except AttributeError: # .group(0) of NoneType for empty strings
        #    if message=False:
        #        fout.write(re.search(r'(.+)\]\]',outline).group(0)[:-2]+'\n')
        except:
            print " ".join([str(element) for element in sys.exc_info()[:2]])
            print line
