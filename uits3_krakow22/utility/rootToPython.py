#filePath = "/home/cehrich/Software/uits3-krakow22/corry-tools/output/exampleData_clusters.root" #60 MB
#filePath = "/home/cehrich/Software/uits3_krakow22-main/corry-tools/output/run456065424_221112065722_uITS3_clusters.root" #700 MB (broken)
filePath = "/home/cehrich/Software/uits3_krakow22-main/corry-tools/output/run456060805_221112060811_uITS3_clusters.root" #18 MB

eventFractionToProcess = 1

file = ROOT.TFile.Open(filePath)
tEvents = file.Get("Event")
tClusters = file.Get("Cluster")

#tClusters.GetListOfBranches().ls() # list detectors
detectors = ["ALPIDE_0","ALPIDE_1","ALPIDE_2","ALPIDE_3","ALPIDE_4"]

events = []

nEvents = tClusters.GetEntriesFast() # to read full file

#progress bar
f = IntProgress(min=0, max=nEvents, description="Converting:")
display(f)
print("Will process ",eventFractionToProcess*100,"% of ", filePath)
numClusters=0
for index,event in enumerate(tClusters):
    if index > nEvents * eventFractionToProcess : break #to limit the number of events to be processed
    myEvent = Event()
    for detector in detectors:
        branch = getattr(event, detector)
        for cluster in branch:
            myClus = Cluster()
            myClus.setData(cluster)
            myEvent.addCluster(myClus)
            numClusters+=1
    events.append(myEvent)
    f.value += 1
    if index%1000 == 0 :
        sys.stdout.write('\r')
        sys.stdout.write("[ %s ] events of %s processed (%.2f%% complete) with %s clusters loaded (%s Mb)" % (index, nEvents, 100*index/nEvents, numClusters, numClusters*6/1000000))
        sys.stdout.flush()
        sleep(0.25)        
print("\n", numClusters, " clusters in", filePath, "that is ", numClusters*6/1000000, "Mb") #48 bits/cluster
f.bar_style = "success"
#tClusters.SetBranchAddress("ALPIDE_0.size()", size)
