import sys,os
import argparse
import time
import ROOT
import numpy as np
import pickle
import tqdm.contrib
from uits3_krakow22.src.Event import Event
from uits3_krakow22.src.Cluster import Cluster
from uits3_krakow22.src.Track import Track

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser(description='''
        Usage: 
        1. Get number of events in raw file with:  /eudaq/bin/euCliReader -i run167000654_210425045725.raw 
        2. Pipe event info from raw file: /eudaq/bin/euCliReader -i run167000654_210425045725.raw -e 0 -E EventNr | python3 extractTimestamps.py 
        Alternative: If you don't want to pipe, save event info to file and give file with python3 extractTimestamps.py -i myFile.txt
        ''',  formatter_class=argparse.RawTextHelpFormatter)
    
    # Optional arguments
    parser.add_argument("-i", "--input", help="Root file containing clusters", default="")
    parser.add_argument("-o", "--output", help="Pickle file to output", default="output.pkl")
    parser.add_argument("-v", "--verbose", help="More printing", action="store_true")
    parser.add_argument("-vv", "--veryverbose", help="Much more printing", action="store_true")
    
    # Parse arguments
    args = parser.parse_args()
    return args

def getInputFile(args):
    if args.__dict__["input"] == "":
        raise Exception("ERROR: No input file provided. Use option -i")     
    else:
        print("INFO: Reading from "+args.__dict__["input"]+"\n")
        filePath = args.__dict__["input"]

    return filePath

if __name__ == "__main__":

    args = parseArguments()
    filePath = getInputFile(args)
    outputPath = args.__dict__["output"]
    print("Opening file")
    file = ROOT.TFile.Open(filePath)
    tEvents = file.Get("Event")
    tClusters = file.Get("Cluster")

    detectors = ["ALPIDE_0","ALPIDE_1","ALPIDE_2","ALPIDE_3","ALPIDE_4"]

    nEvents = tClusters.GetEntriesFast() # to read full file
    print("Going to process ", nEvents, " events.")
    myEvent = Event()
    myClus = Cluster()
    with open(outputPath, 'wb') as f:
        for index,event in tqdm.contrib.tenumerate(tClusters):
            #if index%1000 == 0 : print("Processed ",index,"/",nEvents," events: ","{:.2f}".format((100*index)/nEvents),"%")
            if index > nEvents : break #to limit the number of events to be processed
            for detector in detectors:
                branch = getattr(event, detector)
                for cluster in branch:
                    myClus.setData(cluster)
                    myEvent.addCluster(myClus)
            myEvent.clearData()
            ##events.append(myEvent)
            #pickle.dump(myEvent, f)
    
    print("Done!")
