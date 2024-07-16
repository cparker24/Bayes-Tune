from .readers import *

LEPdir = '/data/rjfgroup/rjf01/cameron.parker/runs/LEPdesign/QVir_Analysis/'

AllData = {}
AllData["Design"] = ReadDesign(LEPdir+"parameters.txt")
AllData["Observables"] = {"EpEm91": {}}
AllData["Observables"]["EpEm91"]["charged-xp"] = {"data": ReadData('/data/rjfgroup/rjf01/cameron.parker/builds/STAT/input/vac-data/Data_ALEPH_EpEm91_charged-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'charged-xp.dat'),
                                                  "emulator": {},
                                                  "plotvars": ["$x_p$","$dN/dx_p$","log","log"],
                                                  "cuts": [np.s_[-2:]]}
AllData["Observables"]["EpEm91"]["pion-xp"] = {"data": ReadData('/data/rjfgroup/rjf01/cameron.parker/builds/STAT/input/vac-data/Data_ALEPH_EpEm91_pion-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'pion-xp.dat'),
                                                  "emulator": {},
                                                  "plotvars": ["$x_p$","$dN/dx_p$","log","log"],
                                                  "cuts": [np.s_[-2:]]}
AllData["Observables"]["EpEm91"]["kaon-xp"] = {"data": ReadData('/data/rjfgroup/rjf01/cameron.parker/builds/STAT/input/vac-data/Data_ALEPH_EpEm91_kaon-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'kaon-xp.dat'),
                                                  "emulator": {},
                                                  "plotvars": ["$x_p$","$dN/dx_p$","log","log"],
                                                  "cuts": [np.s_[-2:]]}
AllData["Observables"]["EpEm91"]["proton-xp"] = {"data": ReadData('/data/rjfgroup/rjf01/cameron.parker/builds/STAT/input/vac-data/Data_ALEPH_EpEm91_proton-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'proton-xp.dat'),
                                                  "emulator": {},
                                                  "plotvars": ["$x_p$","$dN/dx_p$","log","log"],
                                                  "cuts": [np.s_[-2:]]}

# defining emulator paths
for system in AllData["Observables"]:
    for obs in AllData["Observables"][system]:
        AllData["Observables"][system][obs]["emulator"]["file"] = "emulators/"+system+obs+"-emulator.sav"
