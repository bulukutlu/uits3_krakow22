import pickle

def readEvents(filename,nEvents=-1):
    if nEvents == -1 : print("Going to process all events.")
    else: print("Going to process",nEvents,"events.")
    i = 0
    with open(filename, "rb") as f:
        while True:
            try:
                events = pickle.load(f)
                for event in events:
                    if nEvents == -1 or i < int(nEvents) :
                        i += 1
                        yield event
                    else:
                        return
            except EOFError : break

def save2pickle(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

def add2pickle(obj, filename):
    with open(filename, 'ab') as outp:  # Appends to file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)