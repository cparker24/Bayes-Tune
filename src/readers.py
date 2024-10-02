from math import sqrt
import numpy as np
import pandas as pd
import pickle as pkl

# reading data format from old style
def ReadData(FileName):
    # Initialize objects
    Result = {}
    Version = ''

    Result["FileName"] = FileName

    # First read all the header information
    for Line in open(FileName):
        Items = Line.split()
        if (len(Items) < 2): continue
        if Items[0] != '#': continue

        if(Items[1] == 'Version'):
            Version = Items[2]
        elif(Items[1] == 'DOI'):
            Result["DOI"] = Items[2:]
        elif(Items[1] == 'Source'):
            Result["Source"] = Items[2:]
        elif(Items[1] == 'System'):
            Result["System"] = Items[2]
        elif(Items[1] == 'Centrality'):
            Result["Centrality"] = Items[2:4]
        elif(Items[1] == 'XY'):
            Result["XY"] = Items[2:4]
        elif(Items[1] == 'Label'):
            Result["Label"] = Items[2:]

    if(Version != '1.0'):
        raise AssertionError('Bad file version number while reading design points')

    XMode = ''
    if(Result["Label"][0:4] == ['x', 'y', 'stat,low', 'stat,high']):
        XMode = 'x'
    elif(Result["Label"][0:5] == ['xmin', 'xmax', 'y', 'stat,low', 'stat,high']):
        XMode = 'xminmax'
    else:
        raise AssertionError('Invalid list of initial columns!  Should be ("x", "y", "stat,low", "stat,high"), or ("xmin", "xmax", "y", "stat,low", "stat,high")')

    # Then read the actual data
    RawData = np.loadtxt(FileName)

    Result["Data"] = {}
    if(XMode == 'x'):
        Result["Data"]["x"] = RawData[:, 0]
        Result["Data"]["y"] = RawData[:, 1]
        Result["Data"]["yerr"] = {}
        Result["Data"]["yerr"]["stat"] = RawData[:, 2:4]
        Result["Data"]["yerr"]["sys"] = RawData[:, 4:]
        Result["SysLabel"] = Result["Label"][4:]
    elif(XMode == 'xminmax'):
        Result["Data"]["x"] = (RawData[:, 0] + RawData[:, 1]) / 2
        Result["Data"]["xerr"] = (RawData[:, 1] - RawData[:, 0]) / 2
        Result["Data"]["y"] = RawData[:, 2]
        Result["Data"]["yerr"] = {}
        Result["Data"]["yerr"]["stat"] = RawData[:, 3:5]
        Result["Data"]["yerr"]["sys"] = RawData[:, 5:]
        Result["SysLabel"] = Result["Label"][5:]

    yerrtot = []
    for i in range(len(Result["Data"]["yerr"]["stat"])):
        yerrtot.append(sqrt(Result["Data"]["yerr"]["stat"][i][0]**2 + Result["Data"]["yerr"]["sys"][i][0]**2))
    Result["Data"]["yerr"]["tot"] = np.array(yerrtot)

    return Result

def ReadDesign(FileName):
    # This is the output object
    Result = {}

    Result["FileName"] = FileName
    df = pd.read_csv(FileName)
   
    # First read all the header information
    Result["Parameter"] = list(df.columns.values)

    # Then read the actual design parameters
    Result["Design"] = df.to_numpy()
    return Result

# old prediction reader
def ReadPrediction(FileName):
    # Initialize objects
    Result = {}
    Version = ''

    Result["FileName"] = FileName

    # First read all the header information
    for Line in open(FileName+".dat"):
        Items = Line.split()
        if (len(Items) < 2): continue
        if Items[0] != '#': continue

        if(Items[1] == 'Version'):
            Version = Items[2]
        elif(Items[1] == 'Data'):
            Result["Data"] = Items[2]
        elif(Items[1] == 'Design'):
            Result["Design"] = Items[2]

    if(Version != '1.0'):
        raise AssertionError('Bad file version number while reading design points')

    # Then read the actual model predictions
    Result["Prediction"] = np.loadtxt(FileName+".dat").T
    Result["Prediction"] = Result["Prediction"][:,~np.all(Result["Prediction"] == 0, axis=0)]
    Result["Error"] = np.loadtxt(FileName+".err").T
    Result["Error"] = Result["Error"][:,~np.all(Result["Prediction"] == 0, axis=0)]
    return Result