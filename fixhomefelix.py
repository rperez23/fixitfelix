#! /usr/bin/python3

import os
import re
import sys
import argparse
import openpyxl
import warnings
import subprocess
from openpyxl.utils.cell import get_column_letter

def getXLF():

    print("")
    while True:
        s3path = input("  Give me your AWS S3 Path: ")
        lscmd  = "aws s3 ls \"" + s3path + "\" | grep xlsx | awk '{print $4}'"
        xlf = os.popen(lscmd).read()
        m = re.search('\.xlsx$',xlf)
        if m:
            break
    print("")

getXLF()
