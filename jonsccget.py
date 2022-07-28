#! /usr/bin/python3

#we will have already downloaded the scc files BUZ_######.scc
#this script will rename to show_s#_e#_fc.scc
#currently 1,174 scc files in s3://s3-fremantle-ccfiles-or-1/Caption Uploads/FAST CHANNELS/

import os
import re
import sys
import time
import argparse
import openpyxl
import warnings
import subprocess
from openpyxl.utils.cell import get_column_letter

tab = "1. Master Metadata"

warnings.simplefilter(action='ignore', category=UserWarning)

#done
def getXLF():

    print("")
    while True:
        s3path = input("  Give me your AWS S3 Path: ")
        lscmd  = "aws s3 ls \"" + s3path + "\" | grep xlsx | awk '{print $4}'"
        xlf = os.popen(lscmd).read()
        time.sleep(5)
        xlf = xlf.strip()

        s3m = re.search("FAST_CHANNEL/$",s3path)
        xlfm = re.search('\.xlsx$',xlf)

        if s3m and xlfm:
            break

    cpcmd = "aws s3 cp \"" + s3path + xlf + "\" ."
    print(" ",cpcmd)
    cpoutput = os.popen(cpcmd)
    time.sleep(5)

    if not os.path.exists(xlf):
        print("  ~~Could not copy xlf file")
        sys.exit(1)



    return xlf, s3path

#done
def openXLF(xlf):

    try:
        workbook = openpyxl.load_workbook(filename=xlf,read_only=True)
    except:
        print("  Cannot open",xlf)
        sys.exit(0)

    #validate that sheet exists
    if not (tab in workbook.sheetnames):
        print(" ",tab,"not in",xlf)
        sys.exit(0)

    #assign the work sheet object
    ws = workbook[tab]

    return workbook, ws

"""
#have not started
def moveSCC(ws,subcol,hncol):

    startrow = 5
    r        = startrow + 1
    startcol = 2
    endcol   = 34

    for c in range(startcol,endcol + 1):
        txt = str(ws.cell(startrow,c).value)
        txt = txt.lower()

        if txt == "house number":
            print("  House Number")
            print("  ============")
            break
        elif txt == "none":
            sys.exit(1)

    while True:

        txt = str(ws.cell(r,c).value)

        if txt == "None":
            break
        else:
            #print(" ",txt)
            #Left off here form the link
        r += 1
"""

#done: will report columns of scc & house number
def getColumns(ws):

    row      = 5
    col      = 2
    endcol   = 34
    hncol    = 0
    subcol   = 0

    while (subcol == 0) or (hncol == 0):

        txt = str(ws.cell(row,col).value)
        txt = txt.lower()

        if txt == "scc filename \n(no extension)":
            subcol = col
        elif txt == "house number":
            hncol = col
        elif txt == "none":
            print("  Could not find columns")
            sys.exit(1)

        col += 1

    #print("SCC :",subcol," HN:",hncol)
    return subcol,hncol



#1) Get the XLF File
xlf,s3path = getXLF()

#2) open the XLF File: get workbook and worksheet
workbook,ws = openXLF(xlf)

#3) get the columns of the scc files, and HouseNumbers:
subcol, hncol = getColumns(ws)

workbook.close()
