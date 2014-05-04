#!/usr/bin/python
import csv
import subprocess
import sys

with open(sys.argv[1], 'rb') as csvfile:
    videolist = csv.reader(csvfile)
    for video in videolist:
        print "Downloading Video"
        p = subprocess.Popen(["wget" , video[int(sys.argv[2])], stdout=subprocess.PIPE)
        result = p.communicate()[0]
        basename = video[int(sys.argv[2])].split("/")[-1]
        p = subprocess.Popen(["./detect.py" , basename], stdout=subprocess.PIPE)
        result = p.communicate()[0]