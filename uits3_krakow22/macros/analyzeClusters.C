#include <iostream>
#include <fstream>
#include "TFile.h"
#include "TCanvas.h"
#include "TTree.h"
#include <TH1.h>
#include <TH2.h>
#include <TSystem.h>

gSystem->AddLinkedLibs("-L /home/berki/Software/corryvreckan/lib -l libCorryvreckanObjects.so");

void analyzeClusters(const std::string filename){
  /// set up I/O
  TFile *f = new TFile(filename.c_str(), "read");
  TTree *tEvent = (TTree*)f->Get("Event");

  TClonesArray*  arrayMappedCA = new TClonesArray("R3BCalifaMappedData",5);
  TBranch *branchMappedCA = tEvent->GetBranch("CalifaMappedData");
  branchMappedCA->SetAddress(&arrayMappedCA);

  Long64_t mappedCAPerEvent = 0;
  Long64_t nEvent = evt->GetEntries();

  R3BCalifaMappedData** mappedCA;

  /// set up variables
  uint64_t  timestamp = 0., timestampPrev = 0.;
  double time = 0., timePrev = 0.;
  double timeStep = 0.;
  double conversionFactor = (50/3.)*1E-9;
  double clock = 60E6;
  UShort_t crystalId = 0;
  /// Output file
  std::ofstream myfile;
  myfile.open ("example.csv");
  myfile << "EventNr,nHits,ID1,Timestamp1,Time1,ID2,Timestamp2,Time2\n";
  
  for(int i=0; i<nEvent; i++){ // Loop over events
    arrayMappedCA->Clear();
    evt->GetEvent(i);
    mappedCAPerEvent = arrayMappedCA->GetEntriesFast();

    if(mappedCAPerEvent>0){ // Look at only filled events
      myfile << i << "," << mappedCAPerEvent << ",";
      mappedCA = new R3BCalifaMappedData*[mappedCAPerEvent];
      for(int p = 0; p < mappedCAPerEvent; p++){
        mappedCA[p] =(R3BCalifaMappedData*)arrayMappedCA->At(p);
        crystalId = (mappedCA[p]->GetCrystalId());
        timestamp = (mappedCA[p]->GetTime());
        time = (static_cast<double>(timestamp))/clock;
        myfile << crystalId << "," << timestamp << "," << time;
      }
      myfile << "\n";
    }
  }
  myfile.close();
}