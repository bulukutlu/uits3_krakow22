#include <iostream>
#include <fstream>
#include "TFile.h"
#include "TCanvas.h"
#include "TTree.h"
#include <TH1.h>
#include <TH2.h>
//#include "R3BCalifaMappedData.h"

class R3BCalifaMappedData : public TObject {
  public:
    // Default Constructor
    R3BCalifaMappedData()
: fCrystalId(0),
    fEnergy(0),
    fNf(0),
    fNs(0),
    fTime(0),
    fError(0)
    {
    };
    
    /** Standard Constructor
     *@param crystalId   Crystal unique identifier
    *@param energy      Total energy deposited in the crystal [GeV]
    *@param nf          Total fast amplitude deposited in the crystal [a.u.]
    *@param ns          Total slow amplitude deposited on the crystal [a.u.]
    *@param time        Time since event start [ns]
    *@param tot         Time over threshold
    **/
    
    R3BCalifaMappedData(UShort_t crystalId, Int_t energy, Int_t nf, Int_t ns, ULong_t time, UChar_t error, UShort_t tot)
  : fCrystalId(crystalId),
    fEnergy(energy),
    fNf(nf),
    fNs(ns),
    fTime(time),
    fError(error),
    fTot(tot) 
    {
    };
    
    //Destructor
    ~R3BCalifaMappedData() { }
    
    //Getters
    inline const UShort_t& GetCrystalId() const { return fCrystalId; }
    inline const Int_t&    GetEnergy()    const { return fEnergy;    }
    inline const Int_t&    GetNf()        const { return fNf;        }
    inline const Int_t&    GetNs()        const { return fNs;        }
    inline const ULong_t&  GetTime()      const { return fTime;      }
    inline const UChar_t&  GetError()     const { return fError;     }	
    inline const UShort_t& GetTot()       const { return fTot;       }  
    
  protected:
    UShort_t fCrystalId; // crystal unique identifier
    Int_t    fEnergy;    // total energy in the crystal
    Int_t    fNf;        // total fast amplitude in the crystal
    Int_t    fNs;        // total slow amplitude in the crystal
    ULong_t  fTime;      // time-stamp (common to all the hits in the event)
    UChar_t  fError;     // bit coded error flag
    UShort_t fTot;       // time-over-threshold
};

void investigateR3B(const std::string filename){
  /// set up I/O
  TFile *f = new TFile(filename.c_str(), "read");
  TTree *evt = (TTree*)f->Get("evt");

  TClonesArray*  arrayMappedCA = new TClonesArray("R3BCalifaMappedData",5);
  TBranch *branchMappedCA = evt->GetBranch("CalifaMappedData");
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