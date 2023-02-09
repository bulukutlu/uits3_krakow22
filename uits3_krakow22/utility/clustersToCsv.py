#!/usr/bin/env python

# clustersToCsv.py
# Date: 20.10.2022
# Author: Berkin Ulukutlu
# ==> Convert text file from corry to csv table containing clusters

import argparse
import fileinput
from tqdm import tqdm 

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser(description='''
        Usage:
        Run corryvreckan clusterizer with TextWriter module. Then:
        python clusterToCsv.py -i run123456_123456_clusters.txt -o run123456_123456_clusters.csv
        ''',  formatter_class=argparse.RawTextHelpFormatter)
    
    # Optional arguments
    parser.add_argument("-i", "--input", help="Txt file input", default="")
    parser.add_argument("-o", "--output", help="CSV file to save to", default="output.csv")
    parser.add_argument("-v", "--verbose", help="More printing", action="store_true")
    parser.add_argument("-vv", "--veryverbose", help="Much more printing", action="store_true")
    
    # Parse arguments
    args = parser.parse_args()
    return args

def getNLines(path):
    def _count_generator(reader):
        b = reader(1024 * 1024)
        while b:
            yield b
            b = reader(1024 * 1024)
    with open(path, 'rb') as fp:
        c_generator = _count_generator(fp.raw.read)
        count = sum(buffer.count(b'\n') for buffer in c_generator)
        return count+1


if __name__ == "__main__":
    # Parse the arguments
    args = parseArguments()

    # Read csv file to pandas dataframe
    path = args.__dict__["input"]
    if path == "" : raise Exception("No input file provided. Use the -i option to give the path of the .txt file")
    print("Reading file",path)
    nLines = getNLines(path)
    print("Found",nLines,"lines")

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
        for line in tqdm(fileinput.input(path),total=nLines):
            if line[0] == "=":
                eventNr = line.replace("=","").replace(" ","").replace("\n","")
            if line[0] == "-":
                detector = line.replace("-","").replace(" ","").replace("\n","")
            if line[0:8] == "Cluster ":
                cluster = eventNr+","+detector+","+line[8:].replace(" ","").replace("(","").replace(")","").replace("\n","")+"\n"
                if args.veryverbose : print(cluster) # print full output if -vv is given 
                w.write(cluster)