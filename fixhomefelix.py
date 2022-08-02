#! /usr/bin/python3

import os
import sys
import argparse
import openpyxl
import warnings
import subprocess
from openpyxl.utils.cell import get_column_letter

def getXLF():

    print("")
    s3path = input("  Give me your AWS S3 Path: ")
    lscmd  = "aws s3 ls \"" + s3path + "\""
    print(lscmd)
    print("")

getXLF()
