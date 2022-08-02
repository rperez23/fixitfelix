#! /usr/bin/python3

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

def getXLF():

    print("")
    while True:
        s3path = input("  Give me your AWS S3 Path: ")
        lscmd  = "aws s3 ls \"" + s3path + "\" | grep xlsx | awk '{print $4}'"
        xlf = os.popen(lscmd).read()
        time.sleep(5)

        xlf = xlf.strip()
        m = re.search('\.xlsx$',xlf)
        if m:
            break

    cpcmd = "aws s3 cp \"" + s3path + xlf + "\" ."
    print(" ",cpcmd)
    cpoutput = os.popen(cpcmd)
    time.sleep(5)

    if not os.path.exists(xlf):
        print("  ~~Could not copy xlf file")
        sys.exit(1)
    print("")

    return xlf

def openXLF(xlf):

    try:
        workbook = openpyxl.load_workbook(filename=xlf)
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


def makeBackup(xlf):
    cpcmd = "cp " + xlf + " 0rig"
    #print("    making backup file")
    os.popen(cpcmd)
    time.sleep(5)
    backupf = "0rig/" + xlf
    if not os.path.exists(backupf):
        print("  ~~Could not make backup file~~")
        sys.exit(1)


#1) Get the XLF File
xlf = getXLF()

#2) copy the XLF to the 0rig directory
makeBackup(xlf)

#3) open the XLF File: get workbook and worksheet
workbook,ws = openXLF(xlf)

#?) close the workbook
#workbook.save(xlf)
workbook.close()
