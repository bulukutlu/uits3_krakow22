#!/usr/bin/env python

# extractTimestamps.py
# Date: 20.10.2022
# Author: Berkin Ulukutlu
# ==> For extracting timestamp info from raw files recorded with ALPIDEs

import sys,os
import argparse
import csv
import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.lines as mlines
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
from matplotlib.patches import Rectangle
import pandas as pd
import numpy as np


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser(description='''
        Usage:
        0. Run the timestamp extraction scripts first to get the csv files
        1. matchEvents.py -i califa_timestamps.csv -ii alpide_timestamps.csv
        ''',  formatter_class=argparse.RawTextHelpFormatter)
    
    # Optional arguments
    parser.add_argument("-i", "--inputCalifa", help="Timestamps file for Califa", default="")
    parser.add_argument("-ii", "--inputAlpide", help="Timestamps file for Alpide", default="")
    parser.add_argument("-o", "--output", help="CSV file to save to", default="output.csv")
    parser.add_argument("-v", "--verbose", help="More printing", action="store_true")
    parser.add_argument("-vv", "--veryverbose", help="Much more printing", action="store_true")
    parser.add_argument("-l", "--limit", help="Max number of events to be matched", default="-1")
    parser.add_argument("-s", "--shift", help="Number of califa trigger to start matching from", default="1")
    # Parse arguments
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # Parse the input arguments
    args = parseArguments()
    filename_califa = args.__dict__["inputCalifa"] #"realData/califa/ITS_0046_timestamps.csv"
    filename_alpide = args.__dict__["inputAlpide"] #"realData/uits/timestamps_run447065242.csv"
    output_file =  args.__dict__["output"]
    if int(args.__dict__["limit"]) != -1:
        limit = int(args.__dict__["limit"])
    else:
        limit = math.inf
    shift = int(args.__dict__["shift"])

    # Global variables
    clock_califa=60E6
    clock_its=80E6

    # Read input files and set up dfs
    # Califa
    print("Reading Califa file: "+filename_califa)
    df_califa = pd.read_csv(filename_califa, skiprows = lambda x: x >= limit+shift or 0 < x < shift)
    df_califa["EventNr"] = df_califa.index
    df_califa["time"] = (df_califa["Timestamp1"]-df_califa["Timestamp1"][0])/clock_califa
    df_califa["isMatched"] = [False for i in range(len(df_califa.index))]
    print("Read "+str(len(df_califa.index))+" events from file")
    
    # Alpide
    print("Reading Alpide file: "+filename_alpide)
    df_its = pd.read_csv(filename_alpide, skiprows = lambda x: x > limit)
    df_its["time"] = (df_its["ALPIDE_plane_0"]-df_its["ALPIDE_plane_0"][0])/clock_its
    df_its["isMatched"] = [False for i in range(len(df_its.index))]
    print("Read "+str(len(df_its.index))+" events from file")

    if int(args.__dict__["limit"]) == -1:
        limit = min(len(df_its.index),len(df_califa.index))
    else:
        limit = int(args.__dict__["limit"])
        if limit > len(df_its.index) or limit > len(df_califa.index):
            limit = min(len(df_its.index),limit = len(df_califa.index))
            print("Given limit exceeds the number of events in given files, taking the full file range "+str(limit)+" instead.")

    
    # Matching algorithm
    isFound = [False for i in range(limit)] 
    event = 1
    prev=0
    isFound[0] = True
    counter = 0
    timeStep = 0
    df_its["trigger_corrected"] = df_its["TriggerNr"]
    time_shift = 0
    timeStep = 0
    for trigger in range(1,limit):
        timeStep = df_califa["time"][trigger] - df_califa["time"][prev]
        eventTimeStep = df_its["time"][event] - df_its["time"][event-1]
        extraEvent = 0
        while eventTimeStep < timeStep*0.95 and df_its["time"][event+1] - df_its["time"][event-1-extraEvent] < timeStep*1.1:
            extraEvent+=1
            if(extraEvent > 5) : sys.exit('ERROR: Found too many consecutive extra events, something probably went wrong!')
            if(args.verbose) : print("ExtraEvent #"+str(extraEvent)+" / Califa trig: "+ str(trigger)+" -timestep: "+str(timeStep)+" / ALPIDE event: "+str(event)+ " -timestep: "+str(eventTimeStep))        
            event+=1
            eventTimeStep = df_its["time"][event] - df_its["time"][event-1-extraEvent]
        if timeStep < 99.5E-6 and eventTimeStep >=99.5E-6:
            counter+=1
            if(args.veryverbose) : print("Too short at "+str(trigger)+ " with " + str(timeStep))
        else:   
            if abs(eventTimeStep - timeStep) < timeStep*0.1 and abs(eventTimeStep - timeStep) < (df_its["time"][event+1] - df_its["time"][event-1-extraEvent] - timeStep):
                df_its.loc[df_its.index==event,"trigger_corrected"] = trigger
                isFound[trigger] = True
                df_its.loc[df_its.index==event,"isMatched"] = True
                event += 1
                prev = trigger
            else:
                #prev = trigger
                counter+=1
                if(args.veryverbose) : print("Not found corresponding event in trigger "+str(trigger)+ " with timeStep "+str(timeStep))

    print("Ran over "+str(trigger+1)+ " triggers and found "+ str(counter)+ " missing triggers.\n")
    print("Saving to file: "+output_file)
    df_output = df_its[["TriggerNr","isMatched","time","trigger_corrected"]]
    df_output.to_csv(output_file)