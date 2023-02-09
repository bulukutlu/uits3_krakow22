#!/usr/bin/env python

# csvToPickle.py
# Date: 20.10.2022
# Author: Berkin Ulukutlu
# ==> Convert text file from corry to csv table containing clusters

import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
import pickle
import math

from uits3_krakow22.src.Event import Event
from uits3_krakow22.src.Cluster import Cluster

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser(description='''
        Usage:
        Run corryvreckan clusterizer with TextWriter module. Then:
        python clusterToCsv.py -i run123456_123456_clusters.txt -o run123456_123456_clusters.csv
        ''',  formatter_class=argparse.RawTextHelpFormatter)
    
    # Optional arguments
    parser.add_argument("-i", "--input", help="Txt file input", default="")
    parser.add_argument("-o", "--output", help="CSV file to save to", default="output.pkl")
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
    if path == "" : raise Exception("No input file provided. Use the -i option to give the path of the .csv file")
    print("Reading file",path)
    #df = pd.read_csv(path)
    #
    # Create array of events        
    events = []
    previousEventNr = -1

    chunksize = 1e6
    nLines = getNLines(path)
    print("Found",nLines,"clusters.")

    outpath = args.__dict__["output"]
    with open(outpath, 'wb') as outp:
        with pd.read_csv(path, chunksize=chunksize) as reader:
            for df in tqdm(reader,total=math.ceil(nLines/chunksize)):
                for index,row in tqdm(df.iterrows(), total=len(df.index), leave=False):
                    cluster = Cluster(detector=row["detector"],
                                    size=row["nPixels"],
                                    localPos=[row["localX"],row["localY"],0],
                                    globalPos=[row["globalX"],row["globalY"],row["globalZ"]],
                                    charge=row["charge"],
                                    split=bool(row["split"]),
                                    colWidth=row["columnWidth"],
                                    rowWidth=row["rowWidth"])
                    
                    if row["eventNr"] != previousEventNr: #new event
                        if previousEventNr != -1 : events.append(event)
                        previousEventNr = row["eventNr"]
                        if len(events) % 1e6 == 0 and len(events) != 0:
                            pickle.dump(events, outp, pickle.HIGHEST_PROTOCOL)
                            #print("Saved 1 Million events to",outpath) 
                            events = []
                        event = Event(timestamp = row["timeStamp"])
                        event.addCluster(cluster)
                    else :
                        event.addCluster(cluster)
                events.append(event)
                #print("Filled",len(events),"events.")

        #Save to pickle file
        pickle.dump(events, outp, pickle.HIGHEST_PROTOCOL)
        print("Saved events to",outpath)        