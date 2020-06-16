#!/usr/bin/env python
import os
import ftfy
import pytesseract
import re
import difflib
import csv
import dateutil.parser as dparser
import io



def pan_fill(text):
    
    file = open("idtext.txt", 'r',encoding='utf-8')
    text = file.read()
    text = ftfy.fix_text(text)
    text = ftfy.fix_encoding(text)
    # text = filter(lambda x: ord(x) < 128, text)
    print(text)
    #Initializing data variable
    name = None
    fname = None
   
    pan = None
    nameline = []
    dobline = []
    panline = []
    text0 = []
    text1 = []
    text2 = []
    # Searching for PAN
    lines = text.split('\n')
    for lin in lines:
        s = lin.strip()
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)

    text1 = list(text1)
    text1 = list(filter(None, text1))
    for words in text1:
        if len(words) == 1:
            text1.remove(words)
    lineno=0 # to start from the first line of the text file.


    for i, jj in enumerate(text1):
        xx = jj.split('\n')
        if ([w for w in xx if re.findall('INC0MLIXDIPARNT| INCOMETAX DEPARTMENT| INCOME TAX DEPARTMENT|INCOME|TAX|GOW|GOVT|GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA|.GOVT| OF INDIA', w)]):
            lineno = i
            # print("check line number",lineno)
            
    # text1 = list(text1)
    # print("line number",lineno)
    text0 = text1[lineno:]
    print(text0) #Contains all the relevant extracted text in form of a list - uncomment to check

    # ####----------Read Database
    with open('./namedb.csv', 'r') as f:
        reader = csv.reader(f)
        newlist = list(reader)    
    newlist = sum(newlist, [])

    # Searching for Name and finding closest name in database
    try:
        for x in text0:
            for y in x.split():
                if(difflib.get_close_matches(y.upper(), newlist)):
                    nameline.append(x)
                    break
    except:
        pass
    try:
        name = nameline[0]
        fname = nameline[1]
        pan = text0[4]

    except:
        pass
        
    try:
        dobline = [item for item in text0 if item not in nameline]
        for x in dobline: # dobline contains the date of birth and the PAN Card number, here we're just interested in DOB
            z = x.split()
            z = [s for s in z if len(s) > 3]
            for y in z:
                if(dparser.parse(y, fuzzy=True)):
                    dob = y
                    panline = dobline[dobline.index(x)+1:]
                    break
    except:
        pass
    # Making tuples of data
    data = {}
    a=[]
    for i in range(0,len(text0),1):
    #  if (text0[i]=="Permanent Account Number"):
        t=re.findall("[A-Z\s]+",text0[i])
        #print(t)
        if t!=[" "] and len(t)==1:
            x=re.match("[A-Z\s]+",text0[i])
            a.append(text0[i])
            print(a)
        if re.match('^[|_A-Z0-9_]+$',text0[i]):
            #print(text0[i])
            pan=text0[i]
    for i in range(0,len(a),1):
        if ((a[0]==("GOVT. OF INDIA") or (a[0]==("” INCOMETAX DEPARTMENT"))) or (a[0]==("! INCOME TAX DEPARTMENT")) or (a[0]=="GC") or (a[0]==("- INCOMETAX DEPARTHENT")) or (a[0]==("INCOME TAX DEPARTMENT C")) or (a[0]==("* INCOME TAX DEPARTMENT i"))):
            #print("2")
            name=a[1]
            if name == "GC":
                print("done")
                name = a[2]
            else:
                name = a[1]
            #fname=a[2]
        else:
            name=a[0]
            # fname=a[1]

    dob=[]    
    pan=[]   
    for i, jj in enumerate(text0):
        pattern = re.compile(r'\s+')
        jj = re.sub(pattern, '',jj)      
        dd=re.findall("\d{2}[/]\d{2}[/]\d{4}|\d{2}\d{2}\d{4}|\d{1}[/]d{2}[/]d{4}",jj)
        if dd!=[" "] and len(dd)==1:
            dob=dd

    for i, jj in enumerate(text0):    
        jj = jj.replace("_", " ")
        jj = jj.replace("&", "8")
        jj = jj.replace("*"," ")
        jj = jj.replace("\"", "")
        jj = jj.replace(";", "") 
        jj = jj.replace(")", "J")
        jj = jj.replace("s","5")
        pattern = re.compile(r'\s+')
        jj = re.sub(pattern, '',jj) 
        jj = re.sub('0$', 'D', jj)
        jj = re.sub('1$', 'I', jj)
        jj = re.sub('2$', 'Z', jj)
        jj = re.sub('3$', 'B', jj)
        jj = re.sub('4$', 'N', jj)
        jj = re.sub('5$', 'J', jj)
        jj = re.sub('6$', 'G', jj)
        jj = re.sub('7$', 'T', jj)
        jj = re.sub('8$', 'B', jj)
        jj = re.sub('9$', 'J', jj)
        jj = re.sub('^0 ', '', jj)
        jj = re.sub('^1', 'I', jj)
        jj = re.sub('^2', 'Z', jj)
        jj = re.sub('^3 ', '', jj)
        jj = re.sub('^4', 'N', jj)
        jj = re.sub('^5', 'J', jj)
        jj = re.sub('^6', 'G', jj)
        jj = re.sub('^7', 'T', jj)
        jj = re.sub('^8', 'B', jj)
        jj = re.sub('^9', 'J', jj)
        panno=re.findall("[A-Z]{5}\d{4}[A-Z]|[A-Z]{6}\d{3}[A-Z]{1}|[A-Z]{4}\d{4}[A-Z]|[a-zA-Z]{5}\d{4}[a-zA-Z]",jj)
        if panno!=[" "] and len(panno)==1:
            pan=jj  
            print("check pan",pan) 
    
    if len(dob)==1:
        print("Date of birth",dob)
    else:
        dob='01/01/1900'
        print("Date of birth",dob)
    dob=str(dob)
    dob = dob.rstrip()
    dob = dob.lstrip()
    dob = dob.replace('l', '/')
    dob = dob.replace('L', '/')
    dob = dob.replace('o', '0')
    dob = dob.replace('I', '/')
    dob = dob.replace('i', '/')
    dob = dob.replace('|', '/')
    dob = dob.replace('\"', '/1')
    dob = dob.replace(" ", "")
    dob = dob.replace("&", "8")
    dob = dob.replace("'", "")
    dob = dob.replace("[", "")
    dob = dob.replace("]", "")
    
    pan=str(pan)
    pan = pan.rstrip()
    pan = pan.replace("|", " ")
    pan = pan.lstrip()
    pan = pan.replace("_", " ")
    pan = pan.replace(".", "")
    pan = pan.replace("&", "8")
    pan = pan.replace("*"," ")
    pan = pan.replace("\"", "")
    pan = pan.replace(";", "")
    pan = pan.replace("[","")
    pan = pan.replace("]", "")
    pan = pan.replace("'","")
    pan = pan.replace("-","")
    pan = pan.replace("€","")
    pan = pan.replace("s","5")
    pan = pan.replace("”","5") 

    
    name_id=0
    for i, jj in enumerate(text0):
        xx = jj.split()
        if [w for w in xx if re.search('(Name|name|NAME|Nmae|[/]Name)$', w)] and name_id==0:
            name_id=i
        
    if name_id!=0:
        print("nameid=",name_id)
        Name_index=name_id+1
        name=text0[Name_index]     
        print("Name=",text0[Name_index])
    else:
        name=text0[1]
        if name =="GC":
            name = text0[2]
        else:
            name = text0[1]     
        print("Name",text0[1])

    name = name.rstrip()
    name = name.lstrip()
    name = name.replace("|", " ")   
    name = name.replace("™“", " ")
    name = name.replace(":", " ")
    name = name.replace("~", " ")
    name = name.replace("8", "B")
    name = name.replace("0", "D")
    name = name.replace("6", "G")
    name = name.replace("1", "I")
    name = name.replace("%", " ")
    name = name.replace("7", " ")
    name = name.replace("“", " ")
    name = name.replace("—", " ")
    lower = lambda name: re.sub('^[a-z]{1}\s', '',name)
    name = lower(name)
    name = re.sub('[^a-zA-Z] +', ' ', name)

    data['ID']= "Pan Card"
    data['Name'] = name
    data['Date of Birth'] = dob
    pan = re.sub('[a-z]{1}|[A-Z]{1}\s',' ',pan)
    data['pid'] = pan
    
    print("+++++++++++++++++++++++++++++++")
    print("ID : ",data['ID'])
    print("|++++++++++++++++++++++++++++++++++++++++++++++++++|")
    print( "NAME : ", name)
    print("|--------------------------------------------------|")
    print("DOB : " , dob)
    print("|--------------------------------------------------|")
    print("PAN NO :", pan)
    print("|++++++++++++++++++++++++++++++++++++++++++++++++++|")

    return data