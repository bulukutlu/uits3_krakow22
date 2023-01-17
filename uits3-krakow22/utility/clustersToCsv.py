#!/usr/bin/env python

# extractTimestamps.py
# Date: 20.10.2022
# Author: Berkin Ulukutlu
# ==> For extracting timestamp info from raw files recorded with ALPIDEs

import sys,os
import argparse
import csv 

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser(description='''
        Usage: 
        1. Get number of events in raw file with:  /eudaq/bin/euCliReader -i run167000654_210425045725.raw 
        2. Pipe event info from raw file: /eudaq/bin/euCliReader -i run167000654_210425045725.raw -e 0 -E EventNr | python3 extractTimestamps.py 
        Alternative: If you don't want to pipe, save event info to file and give file with python3 extractTimestamps.py -i myFile.txt
        ''',  formatter_class=argparse.RawTextHelpFormatter)
    
    # Optional arguments
    parser.add_argument("-i", "--input", help="Txt file input", default="")
    parser.add_argument("-o", "--output", help="CSV file to save to", default="output.csv")
    parser.add_argument("-v", "--verbose", help="More printing", action="store_true")
    parser.add_argument("-vv", "--veryverbose", help="Much more printing", action="store_true")
    
    # Parse arguments
    args = parser.parse_args()
    return args

def getInputFile(args):
    if args.__dict__["input"] == "":
        print("INFO: No input file provided so reading with stdin\n")
        lines = sys.stdin.readlines()
    else:
        print("INFO: Reading from "+args.__dict__["input"]+"\n")
        with open(args.__dict__["input"]) as f:
            lines = f.readlines()
    return lines

def getEvents(lines):
    # find locations of the starts of real events (ignoring status events)
    events = [i-3 for i,x in enumerate(lines) if x=="  <Description>ITS3global</Description>\n"]
    return events

def getDAQCount(lines,event):
    DAQ_COUNT = int(lines[event+13][10:-8])
    return DAQ_COUNT

def parseEvent(lines,event,DAQ_COUNT):
    # Position helpers
    target = [7,8,10]
    margin_beg = [8,10,11]
    margin_end = [8,10,30]
    # Get information from each event
    line = event + 14
    data = []
    # Get EventNr
    data += [lines[line+target[0]][margin_beg[0]+6:-(margin_end[0]+2)]]
    # Get TriggerNr
    data += [lines[line+target[1]][margin_beg[1]+6:-(margin_end[1]+2)]]
    # Go over ALPIDEs and extract the timestamp (in decimal format)
    for daq in range(DAQ_COUNT):
        line = event + 14 + daq*13
        data += [lines[line+target[2]][margin_beg[2]+6:-(margin_end[2]+2)]]
    return data


if __name__ == "__main__":
    # Parse the arguments
    args = parseArguments()

    # Read input
    lines = getInputFile(args)

    # Header line for the csv file
    header = "eventNr,detector,localX,localY,globalX,globalY,globalZ,charge,split,nPixels,columnWidth,rowWidth,timeStamp"

    # Print stuff for debugging if -v is used
    if(args.verbose) :
        print("You are running the script with arguments:")
        for a in args.__dict__:
            print("\t-> " + str(a) + ": " + str(args.__dict__[a]))
        print("")
    
    # Extract and write to csv file
    if args.__dict__["output"] == "output.csv":
        output_file_name = "output.csv"
    else:
        output_file_name = args.__dict__["output"]

    with open(output_file_name, 'w') as w:
        w.write(header+"\n")
        for line in lines:
            if line[0] == "=":
                eventNr = line.replace("=","").replace(" ","").replace("\n","")
            if line[0] == "-":
                detector = line.replace("-","").replace(" ","").replace("\n","")
            if line[0:8] == "Cluster ":
                cluster = eventNr+","+detector+","+line[8:].replace(" ","").replace("(","").replace(")","").replace("\n","")+"\n"
                if args.veryverbose : print(cluster) # print full output if -vv is given 
                w.write(cluster)