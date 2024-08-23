import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
from .emulator_BAND import EmulatorBAND
import dill
import pandas as pd
from scipy import optimize

# used to trim ranges on observables after reading in
def trimRange(datInput, slc):
    datInput["predictions"]["Prediction"]=np.delete(datInput["predictions"]["Prediction"],slc,1)
    datInput["predictions"]["Error"]=np.delete(datInput["predictions"]["Error"],slc,1)
    datInput["data"]["Data"]["x"]=np.delete(datInput["data"]["Data"]["x"],slc)
    datInput["data"]["Data"]["xerr"]=np.delete(datInput["data"]["Data"]["xerr"],slc)
    datInput["data"]["Data"]["y"]=np.delete(datInput["data"]["Data"]["y"],slc)
    datInput["data"]["Data"]["yerr"]["stat"]=np.delete(datInput["data"]["Data"]["yerr"]["stat"],slc,0)
    datInput["data"]["Data"]["yerr"]["sys"]=np.delete(datInput["data"]["Data"]["yerr"]["sys"],slc,0)
    datInput["data"]["Data"]["yerr"]["tot"]=np.delete(datInput["data"]["Data"]["yerr"]["tot"],slc,0)

def trimRanges(ThisData):
    for system in ThisData["Observables"]:
        for obs in ThisData["Observables"][system]:
            for cut in ThisData["Observables"][system][obs]["cuts"]:
                trimRange(ThisData["Observables"][system][obs], cut)

def updateCuts(ThisData, valData):
    for system in ThisData["Observables"]:
        for obs in ThisData["Observables"][system]:
            valData["Observables"][system][obs]["cuts"] = ThisData["Observables"][system][obs]["cuts"]

# trimming bad points
def trimPoints(points, ThisData):
    points.sort(reverse=True)

    # trimming points in the design array
    ThisData["Design"]["Design"] = np.delete(ThisData["Design"]["Design"], points, 0)

    # going through the datInput
    for system in ThisData["Observables"]:
        for obs in ThisData["Observables"][system]:
            ThisData["Observables"][system][obs]["predictions"]["Prediction"] = np.delete(ThisData["Observables"][system][obs]["predictions"]["Prediction"], points, 0)

# building a pkl files for all observables
def buildObsPkls(ThisData):
    design = ThisData["Design"]["Design"]
    npoints = len(design)

    for system in ThisData["Observables"]:
        for obs in ThisData["Observables"][system]:
            predictions = ThisData["Observables"][system][obs]["predictions"]["Prediction"]
            errors = ThisData["Observables"][system][obs]["predictions"]["Error"]
            totalDict = {}

            # loop over design points in the dir
            for i in range(npoints):
                tempArray = [predictions[i], errors[i]]
                totalDict[str(i)] = {"parameter": np.array(design[i]), "obs": np.array(tempArray)}

            picklefile = "temp-pkls/" + system + obs + ".pkl"
            with open(picklefile, 'wb') as handle:
                pkl.dump(totalDict, handle, protocol = 4)

            ThisData["Observables"][system][obs]["predpkl"] = picklefile

# turning data dict into a pkl for reading in
def buildDataPkl(ThisData, logTrain):
    tempData = []
    tempErrs = []
    for system in ThisData["Observables"]:
        for obs in ThisData["Observables"][system]:
            Result = ThisData["Observables"][system][obs]["data"]
            for i in range(len(Result["Data"]["y"])):
                tempData.append(Result["Data"]["y"][i])
                tempErrs.append(Result["Data"]["yerr"]["tot"][i])

    totalDict = {"0": {"obs": np.log(np.array([tempData,tempErrs]) + 1e-30)}}

    picklefile = "temp-pkls/data.pkl"
    with open(picklefile, 'wb') as handle:
        pkl.dump(totalDict, handle, protocol = 4)

    ThisData["datapkl"] = "temp-pkls/data.pkl"

# training emulators for each obs
def trainEmulators(model_par, ThisData, logTrain):
    for system in ThisData["Observables"]:
        for obs in ThisData["Observables"][system]:
            ThisData["Observables"][system][obs]["emulator"]["emu"] = EmulatorBAND(ThisData["Observables"][system][obs]["predpkl"], model_par, method='PCSK', logTrafo=logTrain, parameterTrafoPCA=False)
            ThisData["Observables"][system][obs]["emulator"]["emu"].trainEmulatorAutoMask()

            with open(ThisData["Observables"][system][obs]["emulator"]["file"], 'wb') as f:
                dill.dump(ThisData["Observables"][system][obs]["emulator"]["emu"], f)

def LogData(ThisData):
    for system in ThisData["Observables"]:
        for obs in ThisData["Observables"][system]:
            ThisData["Observables"][system][obs]["data"]["Data"]["x"]=np.log(ThisData["Observables"][system][obs]["data"]["Data"]["x"] + 1e-30)
            ThisData["Observables"][system][obs]["data"]["Data"]["xerr"]=np.log(ThisData["Observables"][system][obs]["data"]["Data"]["xerr"] + 1e-30)
            ThisData["Observables"][system][obs]["data"]["Data"]["y"]=np.log(ThisData["Observables"][system][obs]["data"]["Data"]["y"] + 1e-30)
            ThisData["Observables"][system][obs]["data"]["Data"]["yerr"]["stat"]=np.log(ThisData["Observables"][system][obs]["data"]["Data"]["yerr"]["stat"] + 1e-30)
            ThisData["Observables"][system][obs]["data"]["Data"]["yerr"]["sys"]=np.log(ThisData["Observables"][system][obs]["data"]["Data"]["yerr"]["sys"] + 1e-30)
            ThisData["Observables"][system][obs]["data"]["Data"]["yerr"]["tot"]=np.log(ThisData["Observables"][system][obs]["data"]["Data"]["yerr"]["tot"] + 1e-30)

# reading emulators for each obs
def readEmulators(ThisData):
    for system in ThisData["Observables"]:
        for obs in ThisData["Observables"][system]:
            with open(ThisData["Observables"][system][obs]["emulator"]["file"], 'rb') as f:
                emu = dill.load(f)
                ThisData["Observables"][system][obs]["emulator"]["emu"] = emu

def getEmuPathList(ThisData):
    emuList = []
    for system in ThisData["Observables"]:
        for obs in ThisData["Observables"][system]:
            emuList.append(ThisData["Observables"][system][obs]["emulator"]["file"])

    return emuList

# getting most like param values
def extract_parameters(data_array, labels, outdir):
    samples = data_array.reshape((-1,data_array.shape[-1]))
    bests = []

    for i,label in enumerate(labels):
        if label == "QSfactor":
            labels[i] = "QS"

    for param_index in range(samples.shape[-1]):
        percentiles1 = np.percentile(samples[:, param_index], [5, 50, 95])
        median1, lower1, upper1 = percentiles1[1], percentiles1[1]-percentiles1[0], percentiles1[2] - percentiles1[1]
        print(f"{labels[param_index]}: {median1:.3f}-{lower1:.3f}+{upper1:.3f}")
        bests.append(median1)

    df = pd.DataFrame([bests],columns=labels)
    df.to_csv(outdir+'parameters.txt',index=False)

    return np.array(bests)

# getting most like param values
def better_extract_parameters(mymcmc, labels, outdir):

    #setting bounds
    bound_min = mymcmc.min
    bound_max = mymcmc.max
    bounds = [(a,b) for (a,b) in zip(bound_min,bound_max)]

    rslt = optimize.differential_evolution(lambda x: -mymcmc.log_likelihood(x.T), 
                                        bounds=bounds,
                                        maxiter=10000,
                                        disp=True,
                                        tol=1e-9,
                                        vectorized=True,
                                        )

    print(rslt.x)

    bests = rslt.x
    labels[3] = "QS"
    bests[3] = (2*bests[6]+0.05) + (bests[2]-(2*bests[6]+0.05))*bests[3]

    for param_index in range(len(bests)):
        print(f"{labels[param_index]}: {bests[param_index]:.3f}")

    df = pd.DataFrame([bests],columns=labels)
    df.to_csv(outdir+'parameters.txt',index=False)

    return np.array(bests)

def ee_extract_parameters(mymcmc, labels, outdir):

    #setting bounds
    bound_min = mymcmc.min
    bound_max = mymcmc.max
    bounds = [(a,b) for (a,b) in zip(bound_min,bound_max)]

    rslt = optimize.differential_evolution(lambda x: -mymcmc.log_likelihood(x.T), 
                                        bounds=bounds,
                                        maxiter=10000,
                                        disp=True,
                                        tol=1e-9,
                                        vectorized=True,
                                        )

    print(rslt.x)

    bests = rslt.x
    labels[1] = "QS"
    bests[1] = (2*bests[3]+0.05) + (bests[0]-(2*bests[3]+0.05))*bests[1]

    for param_index in range(len(bests)):
        print(f"{labels[param_index]}: {bests[param_index]:.3f}")

    df = pd.DataFrame([bests],columns=labels)
    df.to_csv(outdir+'parameters.txt',index=False)

    return np.array(bests)

# sets some universal plot characteristics
def makeplot(ThisData, plotname, indir, samples=None, logTrain=False):
    for system in ThisData["Observables"]:
        Nobs = len(ThisData["Observables"][system])
        figure, axes = plt.subplots(figsize = (3*Nobs, 5), ncols = Nobs, nrows = 2)

        for i, obs in enumerate(ThisData["Observables"][system]):
            axes[0][i].set_title(obs)
            axes[1][i].set_xlabel(ThisData["Observables"][system][obs]["plotvars"][0])
            axes[0][i].set_ylabel(ThisData["Observables"][system][obs]["plotvars"][1])
            axes[1][i].set_ylabel(r"ratio")
            
            DX = ThisData["Observables"][system][obs]["data"]["Data"]["x"]
            DY = ThisData["Observables"][system][obs]["data"]["Data"]["y"]
            DE = ThisData["Observables"][system][obs]["data"]["Data"]["yerr"]["tot"]

            if plotname == "Priors":
                linecount = len(ThisData["Observables"][system][obs]['predictions']["Prediction"])
                for i2, y in enumerate(ThisData["Observables"][system][obs]['predictions']["Prediction"]):
                    axes[0][i].plot(DX, y, 'b-', alpha=10/linecount, label="JETSCAPE" if i2==0 else '')
                    axes[1][i].plot(DX, y/DY, 'b-', alpha=10/linecount, label="JETSCAPE" if i2==0 else '')
            else:
                trimmedsamples = samples[np.random.choice(range(len(samples)), 1000), :]
                linecount = len(trimmedsamples)
                for i2, point in enumerate(trimmedsamples):
                    y = ThisData["Observables"][system][obs]["emulator"]["emu"].predict(point)
                    axes[0][i].plot(DX, np.exp(y[0]) if logTrain else y[0], 'b-', alpha=10/linecount, label="JETSCAPE" if i2==0 else '')
                    axes[1][i].plot(DX, np.exp(y[0])/DY if logTrain else y[0]/DY, 'b-', alpha=10/linecount, label="JETSCAPE" if i2==0 else '')
            
            axes[0][i].errorbar(DX, DY, yerr = DE, fmt='ro', label="Measurements", color='black')
            axes[1][i].plot(DX, 1+(DE/DY), 'b-', linestyle = '--', color='red')
            axes[1][i].plot(DX, 1-(DE/DY), 'b-', linestyle = '--', color='red')
            axes[1][i].axhline(y = 1, linestyle = '--')
            axes[0][i].set_xscale(ThisData["Observables"][system][obs]["plotvars"][2])
            axes[1][i].set_xscale(ThisData["Observables"][system][obs]["plotvars"][2])
            axes[0][i].set_yscale(ThisData["Observables"][system][obs]["plotvars"][3])
            axes[1][i].set_ylim([0,2])

        plt.tight_layout()
        figure.subplots_adjust(hspace=0)
        figure.savefig(indir+system+plotname+'.pdf', dpi = 192)
        # figure

#running validation
def validationPlots(valData, AllData, indir, logTrain = False):
    for system in AllData["Observables"]:
        Nobs = len(AllData["Observables"][system])
        figure, axes = plt.subplots(figsize = (3*Nobs, 5), ncols = Nobs, nrows = 1)

        for i, obs in enumerate(AllData["Observables"][system]):
            axes[i].set_title(obs)
            axes[i].set_xlabel(valData["Observables"][system][obs]["plotvars"][0])
            axes[i].set_ylabel(r"emu/MC")

            DX = AllData["Observables"][system][obs]["data"]["Data"]["x"]
            linecount = len(valData["Design"]["Design"])
            for i2, point in enumerate(valData["Design"]["Design"]):
                y1 = AllData["Observables"][system][obs]["emulator"]["emu"].predict(point)
                y2 = valData["Observables"][system][obs]['predictions']['Prediction'][i2]
                axes[i].plot(DX, np.exp(y1[0])/y2, 'b-', alpha=10/linecount)
            
            axes[i].axhline(y = 1, linestyle = '--')
            axes[i].set_xscale(valData["Observables"][system][obs]["plotvars"][2])
            axes[i].set_ylim([0,2])

        plt.tight_layout()
        figure.subplots_adjust(hspace=0)
        figure.savefig(indir+system+'Validation.pdf', dpi = 192)
        # figure