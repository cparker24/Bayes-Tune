from math import sqrt
from pathlib import Path
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

# turning data dict into a pkl for reading in
def buildDataPkl(Results):
    tempData = []
    tempErrs = []
    for Result in Results:
        for i in range(len(Result["Data"]["y"])):
            tempData.append(Result["Data"]["y"][i])
            tempErrs.append(Result["Data"]["yerr"]["tot"][i])

    totalDict = {"0": {"obs": np.array([tempData,tempErrs])}}

    picklefile = "data/data.pkl"
    with open(picklefile, 'wb') as handle:
        pkl.dump(totalDict, handle, protocol = 4)

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
    for Line in open(FileName):
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
    Result["Prediction"] = np.loadtxt(FileName).T
    return Result

'''
# building a pkl file for an observable
def buildObsPkl(designDir, obsName, histname, npoints):
    designPath = Path(designDir)
    paramsPath = designPath / "QVir_Analysis" / "parameters.txt"
    design = pd.read_csv(str(paramsPath)).to_numpy()

    totalDict = {}

    if "LEP" in designDir:
        rootPath = Path("totals.root")
    else:
        rootPath = Path("root/totals.root")

    # loop over design points in the dir
    for i in range(npoints):
        rootpath = designPath / "points" / str(i) / rootPath
        rootfile = ROOT.TFile(str(rootpath))
        hist = rootfile.Get(histname)
        array = buildArray(hist)

        # handling xp spectra gaps
        if "LEP" in designDir:
            x = np.where(array[0] == 0)
            if x != 0:
                array = np.delete(array,x,axis = 1)

        totalDict[str(i)] = {"parameter": design[i], "obs": array}
    
    print(totalDict)

    picklefile = "preds/" + obsName + ".pkl"
    with open(picklefile, 'wb') as handle:
        pkl.dump(totalDict, handle, protocol = 4)

# builds array for pkl file from a root histogram
def buildArray(hist):
    nbins = hist.GetNbinsX()
    binList = []
    errorList = []

    for i in range(nbins):
        binList.append(hist.GetBinContent(i+1))
        errorList.append(0.0)

    return np.array([binList,errorList])
    '''
