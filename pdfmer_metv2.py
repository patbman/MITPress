# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 10:27:39 2016

@author: patrickbowden
"""
#!/usr/bin/python
import xml.etree.ElementTree as ET
import glob
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import NameObject, createStringObject
from pdfrw import PdfReader, PdfWriter
import sys
import getopt
import subprocess
import configparser
import time

def cparse(co,ho):
    
    
    config=configparser.ConfigParser()
    config.read(co)
    out=config.get('Dir','out')
    inp=config.get('Dir','in')
    cov=config.get('Files','cover')
    right=config.get('Files','copyright')
    xm=config.get('Files','xml')
   # print(out,inp,cov,right,xm)
    xmlp(cov,inp,out,ho,right,xm)

def xmlp(c,loi,loo,ho,co,xm):

    if os.path.isdir(loi)==True:
        os.chdir(loi)
    elif os.path.isdir(loi)==False:
        os.chdir(loi)
      
    for h in os.listdir():
        if h.endswith('xml'):
            xm=h
            break
        else:
            pass
    if xm == None:
        print('no xml file given or found in input directory')
        exit()
    e=ET.parse(xm).getroot()

    for j in e.findall('entry'):
        p=j.find('part').text
        t=j.find('title').text
        a=j.findtext('author')
        m=glob.glob('*'+str(p))
        for i in m:
            if i in m:
                if os.path.isfile(i):
                    print('processing ' + p)
                    mer(c,p,t,a,m,loo,ho,loi,co)
                else:
                    pass
        
def mer(c,pa,ti,au,fi,loo,ho,loi,co):        
    '''Cover merger'''
  
    writer = PdfWriter()
    if c.endswith('.pdf'):
        writer.addpages(PdfReader(c).pages)
    
    elif not c.endswith('.pdf'):
        writer.addpages(PdfReader(c +'.pdf').pages)
    

    files = [v for v in os.listdir() if v.endswith('.pdf')]
    
    if co.endswith('.pdf'):
        writer.addpages(PdfReader(co).pages)
    elif not co.endswith('.pdf'):

        writer.addpages(PdfReader(co +'.pdf').pages)
    for fname in sorted(files):
        if not fname.startswith(c):
            if not fname.startswith(co):
                writer.addpages(PdfReader(os.path.join(fname)).pages)

    writer.write(ti + '.pdf')
    meta(pa,ti,au,fi,loo,ho,loi)
    
def meta(pa,ti,au,fi,loo,ho,loi):
    OUTPUT = ti+'.pdf'
    INPUTS = [ti+'.pdf',]
    
    if au == None:
        au = ''
    else:
        pass
    
    output = PdfFileWriter()
    
    infoDict = output._info.getObject()
    infoDict.update({
        NameObject('/Title'): createStringObject(ti),
        NameObject('/Author'): createStringObject(str(au)),
       # NameObject('/Subject'): createStringObject(su),
       #NameObject('/'): createStringObject('Fit'),
       # NameObject('/Fit'): createStringObject('Fit-to-page')
    })

    inputs = [PdfFileReader( open(i, "rb")) for i in INPUTS]
    for input in inputs:
        for page in range(input.getNumPages()):
            output.addPage(input.getPage(page))
            #output.addLink(page,0,rect='[0,0,0,0]',border=None,fit='/Fit')
    if os.path.isdir(ho+'/'+loo)==True:
        os.chdir(ho + '/' + loo)
    elif os.path.isdir(ho+'/'+loo)==False:
        os.chdir(loo)
    #pdf.generic.Destination(title='test',page=1,typ='/Fit')
    output.setPageLayout('/SinglePage')
    outputStream = open(OUTPUT, 'wb')
    #output.addLink(0,0,rect='[0,0,0,0]',border=None,fit='/Fit')
    output.write(outputStream)
    outputStream.close()
    
    if os.path.isdir(loi)==True:
        os.chdir(loi)
    elif os.path.isdir(loi)==False:
        os.chdir(ho+'/'+loi)
    os.remove(ti+'.pdf')
    if os.name == 'posix':
        
        subprocess.call(ho+'cpdf/mac/cpdf.sh -fit-window true ' + ho+'/'+loo+ti + ' -o ' + ho+'/'+loo+ti,shell=True)
    elif os.name == 'nt':
        subprocess.call(ho+'cpdf/win/cpdf.exe -fit-window true ' + ho+'/'+loo+ti + ' -o ' + ho+'/'+loo+ti,shell=True)
        

def main():
    ho=os.getcwd()
    
    '''
    locin = input("input directory default is current directory: ") or 'input/'
    locout = input("output directory default is current directory: ") or 'output/'
    cover = input("input the name of the cover file: ")
    '''
   
    
    locin ='input/'
    locout = 'output/'
    cover = None
    copy = None
    con=None
    xm=None
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hi:o:C:r:xm:con:')
    except getopt.GetoptError:
        print('Error')
    for opt, arg in opts:
        if opt == '-h':
            print('''            -h = help screen
            -i = input directory
            -o = output directory
            -con = directory to config file
            -C = cover file
            -r = copyright file
            -xml = path to xml file
            ''')
            sys.exit()
        elif opt in ('-i'):
            locin = arg
        elif opt in ('-o'):
            locout = arg
        elif opt in ('-C'):
            cover = arg
        elif opt in ('-r'):
            copy = arg
        elif opt in ('-con'):
            con=arg
        elif opt in ('-xml'):
            xm=arg

    if con != None:

        cparse(con,ho)
    elif con == None:
        if cover == None and copy == None:
            print('no Cover and copyright file given')
            exit()
        elif cover != None and copy != None:
            xmlp(cover,locin,locout,ho,copy,xm)
    #copy = input("input the name of the copyright file: ")

    
    
   
      
    
    
    
    
main()