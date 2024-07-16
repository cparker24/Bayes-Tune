from .readers import *

dataDir = '/data/rjfgroup/rjf01/cameron.parker/builds/STAT/input/vac-data/'
LEPdir = '/data/rjfgroup/rjf01/cameron.parker/runs/LEPdesign/QVir_Analysis/'
LHCdir = '/data/rjfgroup/rjf01/cameron.parker/runs/LHC2760design/QVir_Analysis/'

AllData = {}
AllData["Design"] = ReadDesign(LEPdir+"parameters.txt")
AllData["Observables"] = {"EpEm91": {}, "PrPr2760": {}}
AllData["Observables"]["EpEm91"]["charged-xp"] = {"data": ReadData('/data/rjfgroup/rjf01/cameron.parker/builds/STAT/input/vac-data/Data_ALEPH_EpEm91_charged-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'charged-xp.dat'),
                                                  "emulator": {},
                                                  "plotvars": ["$x_p$","$dN/dx_p$","log","log"],
                                                  "cuts": [np.s_[-5:]]}
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
AllData["Observables"]["EpEm91"]["proton-xp"] = {"data": ReadData('/data/rjfgroup/rjf01/cameron.parker/builds/STAT/input/vac-data/Data_ALEPH_EpEm91_inc-jets.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'jet.dat'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$dN/dp_T$","linear","linear"],
                                                  "cuts": [np.s_[-2:]]}


AllData["Observables"]["PrPr2760"]["charged-pT"] = {"data": ReadData(dataDir+'Data_CMS_PrPr2760_charged-hads.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'HadronSpectraPrediction.dat'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$d^2N/dp_Td\eta$","log","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["pion-pT"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr2760_pions.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'PionSpectraPrediction.dat'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$1/(N_{ev}*2\pi*p_T)d^2N/dp_Tdy$","log","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["kaon-pT"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr2760_kaons.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'KaonSpectraPrediction.dat'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$1/(N_{ev}*2\pi*p_T)d^2N/dp_Tdy$","log","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["proton-pT"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr2760_protons.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'ProtonSpectraPrediction.dat'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$1/(N_{ev}*2\pi*p_T)d^2N/dp_Tdy$","log","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["jets-R2"] = {"data": ReadData(dataDir+'Data_CMS_PrPr2760_jets-2.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'JetSpectraPredictionR2.dat'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$d^2\sigma/dp_Td\eta$","linear","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["jets-R3"] = {"data": ReadData(dataDir+'Data_CMS_PrPr2760_jets-3.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'JetSpectraPredictionR3.dat'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$d^2\sigma/dp_Td\eta$","linear","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["jets-R4"] = {"data": ReadData(dataDir+'Data_CMS_PrPr2760_jets-4.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'JetSpectraPredictionR4.dat'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$d^2\sigma/dp_Td\eta$","linear","log"],
                                                  "cuts": []}

# defining emulator paths
for system in AllData["Observables"]:
    for obs in AllData["Observables"][system]:
        AllData["Observables"][system][obs]["emulator"]["file"] = "emulators/"+system+obs+"-emulator.sav"
