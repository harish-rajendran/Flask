from flask import Flask,jsonify
import yaml
import MySQLdb
import MySQLdb.cursors
import json
import sys
import csv
from config import Config
from DBsingleTon import DBsingleTon 
from pyPdf import PdfFileReader,PdfFileWriter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

dbaccess = DBsingleTon()

db = dbaccess.db_conn()

def validate(values):
    vid = values['vendorid'] 
    sname = values['storename']
    sid = values['storeid']
    city = values['city']
    branch = values['branch']
    state = values['state']
    if len(sname)>0 and len(sid)>0 and len(city)>0 and len(branch)>0 and len(state)>0 :
        return True
    else:
        return False


def check(values):
    vid = values['vendorid']
    sid = values['storeid']
    cursor = db.cursor()
    cursor.execute("SELECT * FROM vendor WHERE vendorid =%s AND storeid = %s" ,(vid,sid))
    db.commit()
    count = cursor.rowcount       
    if count == 0:
        return True
    else:
        message = json.dumps({"status":"NOT OK","message":"Store already exists"})
        return message


def insert(values):
    vid = values['vendorid'] 
    sname = values['storename']
    sid = values['storeid']
    city = values['city']
    branch = values['branch']
    state = values['state']
    cursor = db.cursor()
    cursor.execute("INSERT INTO vendor(vendorid,storename,storeid,city,branch,state)VALUES(%s,%s,%s,%s,%s,%s)",(vid,sname,sid,city,branch,state))
    db.commit()
    message = json.dumps({"status":"OK","message":"SIGN IN SUCCESS"})
    return message


def fetch(data):
    vid = data['vendorid']
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM vendor WHERE vendorid=%s ",(vid)) 
    rows = cursor.fetchall()
    db.commit()
    s={}
    d={}
    cnt=0
    for row in rows:
        d['vendorid']=row['vendorid']
        d['storename']=row['storename']
        d['storeid']=row['storeid']
        d['city']=row['city']
        d['branch']=row['branch']
        d['state']=row['state']
        s[str(cnt)]=d
        cnt=cnt+1
    #print json.dumps(s)
    return json.dumps(s)



def fetchone(datas):
    vid=datas['vendorid']
    if type(datas['storeid'])==list:
        c=len(datas['storeid'])
        count=0
        s={}
        d={}
        #print c
        while count < c :
            sid = datas['storeid'][count]
            #print vid,sid
            cursor=db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM vendor WHERE vendorid=%s AND storeid =%s",(vid,sid))
            row = cursor.fetchone()
            db.commit()
            s[str(count)]=d
            d['vendorid']=row['vendorid']
            d['storename']=row['storename']
            d['storeid']=row['storeid']
            d['city']=row['city']
            d['branch']=row['branch']
            d['state']=row['state']
            s[str(count)]=d
            count+=1
            #print s
            #print count
        return json.dumps(s)
    else:
        #print type(datas)
        sid = datas['storeid']
        #print vid,type(sid)
        cursor=db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT vendorid,storename,storeid,city,branch,state FROM vendor WHERE vendorid=%s AND storeid =%s",(vid,sid))
        row = cursor.fetchone()
        #print row
        db.commit()
        name = json.dumps(row)
        return name


        
def update(values):
    vid = values['vendorid'] 
    sname = values['storename']
    sid = values['storeid']
    city = values['city']
    branch = values['branch']
    state = values['state']
    cursor = db.cursor()
    cursor.execute("UPDATE vendor SET storename=%s,storeid=%s,city=%s,branch=%s,state=%s WHERE vendorid=%s",(sname,sid,city,branch,state,vid)) 
    db.commit()
    message = json.dumps({"status":"OK","message":"UPDATED SUCCESSFULLY"})
    return message


def delete(value):
    vid = value['vendorid']
    if type(value['storeid'])==list:
        c=len(value['storeid'])
        print c
        count=0
        while count <c : 
            sid = value['storeid'][count]
            #print sid
            cursor=db.cursor()
            cursor.execute("DELETE FROM vendor WHERE storeid=%s",(sid,))
            db.commit()
            count+=1
        message = json.dumps({"status":"OK","message":"DELETED SUCCESSFULLY"})
        return message

    else:
        sid = value['storeid']
        cursor=db.cursor()
        cursor.execute("DELETE FROM vendor WHERE storeid = %s " , (sid))
        db.commit()
        message = json.dumps({"status":"OK","message":"DELETED SUCCESSFULLY"})
        return message

def excelsheet(value):
    vid = value['vendorid']
    cursor=db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT vendorid,storename,storeid,city,branch,state FROM vendor WHERE vendorid=%s", (vid,))
    result=cursor.fetchall()
    fp = open('sheet.csv', 'w')
    myFile = csv.writer(fp, lineterminator='\n')
    myFile.writerows([result[0].keys()])
    for row in result:
        myFile.writerows([row.values()])
    fp.close()
    message = json.dumps({"status":"OK","message":"File Saved Successfully"})
    return message 

def pdf(value):
    vid = value['vendorid']
    doc = SimpleDocTemplate("details.pdf", pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
    doc.pagesize = landscape(A4)
    magName = "Store Details "
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                       ('TEXTCOLOR',(1,1),(-2,-2),colors.black),
                       ('VALIGN',(0,0),(0,-1),'TOP'),
                       ('TEXTCOLOR',(0,0),(0,-1),colors.black),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,-1),(-1,-1),colors.black),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ])
    cursor=db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT vendorid,storename,storeid,city,branch,state FROM vendor WHERE vendorid=%s ", (vid,))
    result=cursor.fetchall()
    #content = file("list.pdf","wb")
    elements=[]
    elements.append(Paragraph(magName, styles["Justify"]))
    values=[]
    values.append(result[0].keys())
    for row in result:
        values.append(row.values())
    #print type(values)
    sheet = getSampleStyleSheet()
    sheet = sheet["BodyText"]
    sheet.wordWrap = 'CJK'
    table=Table(values, hAlign='CENTER')
    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    return True

def water():
    c= canvas.Canvas("watermark.pdf") 
    c.setFont("Courier", 60)
    c.setFillGray(0.5,0.5)
    c.saveState() 
    c.translate(500,100) 
    c.rotate(45) 
    c.drawCentredString(0, 300, " 1000 LOOKZ ")
    c.restoreState() 
    c.save() 
    output = PdfFileWriter() 
    input1 = PdfFileReader(file("details.pdf", "rb")) 
    #print "title = %s" % (input1.getDocumentInfo().title)
    page1 = input1.getPage(0)
    watermark = PdfFileReader(file("watermark.pdf", "rb"))
    page1.mergePage(watermark.getPage(0))
    output.addPage(page1)
    outputStream = file("watermarked_pdf.pdf", "wb")
    output.write(outputStream) 
    outputStream.close()
    return "successs"

