import numpy as np 
import fitz
import re

def ola_bill(a):

    index_name=0
    index_mob=0
    index_date=0
    index_sid=0

    for i,jj in enumerate(a):
        xx = jj.split()
        if [w for w in xx if re.search('(Name|Name(s)|given|name|names|Names)$', w)]:
            index_name=i
            x=re.split("Customer Name",a[i])
    name=x[1]
    print("the travelled person name is ",name)
    for i,jj in enumerate(a):
        xx = jj.split()
        if [w for w in xx if re.search('(Mobile|Number)$', w)]:
            index_mob=i
            y=re.split("Mobile Number",a[i])

    mob=y[1]
    print("the travelled person mobile number is ",mob)
    for i,jj in enumerate(a):
        xx = jj.split()
        if [w for w in xx if re.search('(Date|date)$', w)]:
            index_date=i
            z=re.split("Invoice Date",a[i])

    date=z[1]
    print("the date of travel is ",date)
    # Invoice Serial Id:DVDJEKW200769
    list1=[]
    list2=[]
    for i,jj in enumerate(a):
        sno=re.findall("[A-Z]{7}\d{6}",jj)
        if sno!=[" "] and len(sno)==1:
            list1.append(sno)    
    serial_id=list1[0][0]
    for i,jj in enumerate(a):
        xx = jj.split()
        if jj=="Total Bill (rounded off)":
            index_date=i
            totalfare=a[i+2]
    print("Total Fare for the trip is " ,totalfare)
    # serial_id=z[1]
    print("the invoice serial id of travel is ",serial_id)
    for i,jj in enumerate(a):
        xx=jj.split()
        time=re.findall("\d{2}:\d{2}\s[A-Z]{2}",jj)
        if time!=[" "] and len(time)==1:
            list2.append(time)    
    time1=list2[0][0]
    time2=list2[1][0]
    # print(time1,time2)
    index_time=0
    b=[]
    for i,jj in enumerate(a):
        xx = jj.split()
        if(jj==time1):
            b.append(i)
        if(jj==time2):
            temp=i
    #         print(temp)
            break
    temp1=b[0]
    print("the pickup address is ")
    for i in range(temp1,temp-1,1):
        print(a[i+1])
    c=[]
    for i,jj in enumerate(a):
        xx = jj.split()
        if(jj==time2):
            c.append(i)
        if(jj=="Ride Fare"):
            temp=i
    #         print(temp)
            break
    # print(temp)
    temp2=c[0]
    print("the Drop address is ")
    for i in range(temp2,temp-1,1):
        print(a[i+1])

file = '/home/ananthu/projects/invoice_extraction/data/ola_bill1.pdf'
doc = fitz.open(file)
page_count = doc.pageCount
#print(page_count)
page =0 

text = str()
while( page < page_count):
    p = doc.loadPage(page)
    page += 1
    text = text + p.getText()
#print(text)
a=[]
lines1 = text.split('\n')
for lin in lines1:
    s = lin.strip()
    s = s.rstrip()
    s = s.lstrip()
    a.append(s)
#print(a)
ola_bill(a)

