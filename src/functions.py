import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
from .emulator_BAND import EmulatorBAND
import dill

# used to trim ranges on observables after reading in
def trimRange(datInput, slc):
    datInput["predictions"]["Prediction"]=np.delete(datInput["pred"]["Prediction"],slc,1)
    datInput["data"]["Data"]["x"]=np.delete(datInput["data"]["Data"]["x"],slc)
    datInput["data"]["Data"]["xerr"]=np.delete(datInput["data"]["Data"]["xerr"],slc)
    datInput["data"]["Data"]["y"]=np.delete(datInput["data"]["Data"]["y"],slc)
    datInput["data"]["Data"]["yerr"]["stat"]=np.delete(datInput["data"]["Data"]["yerr"]["stat"],slc,0)
    datInput["data"]["Data"]["yerr"]["sys"]=np.delete(datInput["data"]["Data"]["yerr"]["sys"],slc,0)

# building a pkl files for all observables
def buildObsPkls(ThisData):
    design = ThisData["Design"]["Design"]
    npoints = len(design)

    for system in ThisData["Observables"]:
        for obs in ThisData["Observables"][system]:
            predictions = ThisData["Observables"][system][obs]["predictions"]["Prediction"]
            totalDict = {}

            # loop over design points in the dir
            for i in range(npoints):
                tempArray = [predictions[i], [0]*len(predictions[i])]
                totalDict[str(i)] = {"parameter": np.array(design[i]), "obs": np.array(tempArray)}

            picklefile = "temp-pkls/" + system + obs + ".pkl"
            with open(picklefile, 'wb') as handle:
                pkl.dump(totalDict, handle, protocol = 4)

            ThisData["Observables"][system][obs]["predpkl"] = picklefile

# turning data dict into a pkl for reading in
def buildDataPkl(ThisData):
    tempData = []
    tempErrs = []
    for system in ThisData["Observables"]:
        for obs in ThisData["Observables"][system]:
            Result = ThisData["Observables"][system][obs]["data"]
            for i in range(len(Result["Data"]["y"])):
                tempData.append(Result["Data"]["y"][i])
                tempErrs.append(Result["Data"]["yerr"]["tot"][i])

    totalDict = {"0": {"obs": np.array([tempData,tempErrs])}}

    picklefile = "temp-pkls/data.pkl"
    with open(picklefile, 'wb') as handle:
        pkl.dump(totalDict, handle, protocol = 4)

    ThisData["datapkl"] = "temp-pkls/data.pkl"

# training emulators for each obs
def trainEmulators(model_par, ThisData):
    model_par = "input/modelDesign.txt"
    for system in ThisData["Observables"]:
        for obs in ThisData["Observables"][system]:
            ThisData["Observables"][system][obs]["emulator"]["emu"] = EmulatorBAND(ThisData["Observables"][system][obs]["predpkl"], model_par, method='PCGP', logTrafo=False, parameterTrafoPCA=False)
            ThisData["Observables"][system][obs]["emulator"]["emu"].trainEmulatorAutoMask()

            with open(ThisData["Observables"][system][obs]["emulator"]["file"], 'wb') as f:
                dill.dump(ThisData["Observables"][system][obs]["emulator"], f)

# reading emulators for each obs
def readEmulators(ThisData):
    for system in ThisData["Observables"]:
        for obs in ThisData["Observables"][system]:
            ThisData["Observables"][system][obs]["emulator"]["emu"] = dill.load(ThisData["Observables"][system][obs]["emulator"]["file"])

# sets some universal plot characteristics
def makeplot(AllData, plotvars, prediction, plotname, indir):
    Nobs = len(AllData["observables"][0][1])
    figure, axes = plt.subplots(figsize = (3*Nobs, 5), ncols = Nobs, nrows = 2)

    for s2 in range(0, Nobs):
        axes[0][s2].set_title(AllData["observables"][0][1][s2])
        axes[0][s2].set_ylabel(plotvars[s2][1])
        axes[1][s2].set_xlabel(plotvars[s2][0])
        axes[1][s2].set_ylabel(r"ratio")
        
        S1 = AllData["systems"][0]
        O  = AllData["observables"][0][0]
        S2 = AllData["observables"][0][1][s2]
        
        DX = AllData["data"][S1][O][S2]['x']
        DY = AllData["data"][S1][O][S2]['y']
        DE = np.sqrt(AllData["data"][S1][O][S2]['yerr']['stat'][:,0]**2 + AllData["data"][S1][O][S2]['yerr']['sys'][:,0]**2)
                
        if plotname == 'Priors':
            linecount = len(prediction[S1][O][S2]['Y'])
            for i, y in enumerate(prediction[S1][O][S2]['Y']):
                axes[0][s2].plot(DX, y, 'b-', alpha=10/linecount, label=plotname if i==0 else '')
                axes[1][s2].plot(DX, y/DY, 'b-', alpha=10/linecount, label=plotname if i==0 else '')
        else:
            linecount = len(prediction[S1][O][S2])
            for i, y in enumerate(prediction[S1][O][S2]):
                axes[0][s2].plot(DX, y, 'b-', alpha=10/linecount, label=plotname if i==0 else '')
                axes[1][s2].plot(DX, y/DY, 'b-', alpha=10/linecount, label=plotname if i==0 else '')
        
        axes[0][s2].errorbar(DX, DY, yerr = DE, fmt='ro', label="Measurements")
        axes[1][s2].plot(DX, 1+(DE/DY), 'b-', linestyle = '--', color='red')
        axes[1][s2].plot(DX, 1-(DE/DY), 'b-', linestyle = '--', color='red')
        axes[1][s2].axhline(y = 1, linestyle = '--')
        axes[0][s2].set_xscale(plotvars[s2][2])
        axes[1][s2].set_xscale(plotvars[s2][2])
        axes[0][s2].set_yscale(plotvars[s2][3])
        axes[1][s2].set_ylim([0,2])

    plt.tight_layout()
    figure.subplots_adjust(hspace=0)
    figure.savefig(indir+plotname+'.pdf', dpi = 192)
    # figure