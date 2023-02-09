import pickle

def readEvents(filename,nEvents=-1):
    i = 0
    with open(filename, "rb") as f:
        while True:
            try:
                events = pickle.load(f)
                for event in events:
                    if nEvents == -1 or i < nEvents:
                        yield event
                        i += 1
            except EOFError:
                break