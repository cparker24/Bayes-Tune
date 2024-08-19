from .readers import *
import copy

dataDir = '/data/rjfgroup/rjf01/cameron.parker/builds/Bayes-Tune/input/data/'
LEPdir = '/data/rjfgroup/rjf01/cameron.parker/runs/LEPdesign/QVir_Analysis/'
LHCdir = '/data/rjfgroup/rjf01/cameron.parker/runs/LHC2760design/QVir_Analysis/'
LHC13000dir = '/data/rjfgroup/rjf01/cameron.parker/runs/LHC13000design/QVir_Analysis/'

AllData = {}
AllData["Design"] = ReadDesign(LHCdir+"parameters.txt")
AllData["Observables"] = {"EpEm91": {}, "PrPr2760": {}, "PrPr13000": {}}
AllData["Observables"]["EpEm91"]["charged-xp"] = {"data": ReadData('/data/rjfgroup/rjf01/cameron.parker/builds/STAT/input/vac-data/Data_ALEPH_EpEm91_charged-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'charged-xp'),
                                                  "emulator": {},
                                                  "plotvars": ["$x_p$","$dN/dx_p$","log","log"],
                                                  "cuts": [np.s_[-7:]]}
AllData["Observables"]["EpEm91"]["pion-xp"] = {"data": ReadData('/data/rjfgroup/rjf01/cameron.parker/builds/STAT/input/vac-data/Data_ALEPH_EpEm91_pion-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'pion-xp'),
                                                  "emulator": {},
                                                  "plotvars": ["$x_p$","$dN/dx_p$","log","log"],
                                                  "cuts": [np.s_[-2:]]}
AllData["Observables"]["EpEm91"]["kaon-xp"] = {"data": ReadData('/data/rjfgroup/rjf01/cameron.parker/builds/STAT/input/vac-data/Data_ALEPH_EpEm91_kaon-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'kaon-xp'),
                                                  "emulator": {},
                                                  "plotvars": ["$x_p$","$dN/dx_p$","log","log"],
                                                  "cuts": [np.s_[-2:]]}
AllData["Observables"]["EpEm91"]["proton-xp"] = {"data": ReadData('/data/rjfgroup/rjf01/cameron.parker/builds/STAT/input/vac-data/Data_ALEPH_EpEm91_proton-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'proton-xp'),
                                                  "emulator": {},
                                                  "plotvars": ["$x_p$","$dN/dx_p$","log","log"],
                                                  "cuts": [np.s_[-2:]]}
AllData["Observables"]["EpEm91"]["jets"] = {"data": ReadData('/data/rjfgroup/rjf01/cameron.parker/builds/STAT/input/vac-data/Data_ALEPH_EpEm91_inc-jets.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'jet'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$dN/dp_T$","linear","linear"],
                                                  "cuts": [np.s_[-2:]]}


AllData["Observables"]["PrPr2760"]["charged-pT"] = {"data": ReadData(dataDir+'Data_CMS_PrPr2760_charged-hads.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'HadronSpectraPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$d^2N/dp_Td\eta$","log","log"],
                                                  "cuts": [np.s_[8:12]]}
AllData["Observables"]["PrPr2760"]["pion-pT"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr2760_pions.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'PionSpectraPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$1/(N_{ev}*2\pi*p_T)d^2N/dp_Tdy$","log","log"],
                                                  "cuts": [np.s_[31:50]]}
AllData["Observables"]["PrPr2760"]["kaon-pT"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr2760_kaons.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'KaonSpectraPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$1/(N_{ev}*2\pi*p_T)d^2N/dp_Tdy$","log","log"],
                                                  "cuts": [np.s_[26:45]]}
AllData["Observables"]["PrPr2760"]["proton-pT"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr2760_protons.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'ProtonSpectraPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$1/(N_{ev}*2\pi*p_T)d^2N/dp_Tdy$","log","log"],
                                                  "cuts": [np.s_[24:43]]}
AllData["Observables"]["PrPr2760"]["jets-R2"] = {"data": ReadData(dataDir+'Data_CMS_PrPr2760_jets-2.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'JetSpectraPredictionR2'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$d^2\sigma/dp_Td\eta$","linear","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["jets-R3"] = {"data": ReadData(dataDir+'Data_CMS_PrPr2760_jets-3.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'JetSpectraPredictionR3'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$d^2\sigma/dp_Td\eta$","linear","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["jets-R4"] = {"data": ReadData(dataDir+'Data_CMS_PrPr2760_jets-4.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'JetSpectraPredictionR4'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$d^2\sigma/dp_Td\eta$","linear","log"],
                                                  "cuts": []}

AllData["Observables"]["PrPr13000"]["pion-pT"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr13000_pions.dat'),
                                                  "predictions": ReadPrediction(LHC13000dir+'PionSpectraPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$1/N_{ev}d^2N/dp_Tdy$","log","log"],
                                                  "cuts": [np.s_[:21]]}
AllData["Observables"]["PrPr13000"]["kaon-pT"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr13000_kaons.dat'),
                                                  "predictions": ReadPrediction(LHC13000dir+'KaonSpectraPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$1/N_{ev}d^2N/dp_Tdy$","log","log"],
                                                  "cuts": [np.s_[:16]]}
AllData["Observables"]["PrPr13000"]["proton-pT"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr13000_protons.dat'),
                                                  "predictions": ReadPrediction(LHC13000dir+'ProtonSpectraPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$1/N_{ev}d^2N/dp_Tdy$","log","log"],
                                                  "cuts": [np.s_[29:39],np.s_[:14]]}
AllData["Observables"]["PrPr13000"]["low-y-jets"] = {"data": ReadData(dataDir+'Data_ATLAS_PrPr13000_low-y-jets.dat'),
                                                  "predictions": ReadPrediction(LHC13000dir+'LowYJetPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$d^2\sigma/dp_Tdy$","log","log"],
                                                  "cuts": [np.s_[-5:]]}
AllData["Observables"]["PrPr13000"]["mid-y-jets"] = {"data": ReadData(dataDir+'Data_ATLAS_PrPr13000_mid-y-jets.dat'),
                                                  "predictions": ReadPrediction(LHC13000dir+'MidYJetPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$d^2\sigma/dp_Tdy$","log","log"],
                                                  "cuts": [np.s_[-5:]]}
AllData["Observables"]["PrPr13000"]["high-y-jets"] = {"data": ReadData(dataDir+'Data_ATLAS_PrPr13000_low-y-jets.dat'),
                                                  "predictions": ReadPrediction(LHC13000dir+'HighYJetPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_T$","$d^2\sigma/dp_Tdy$","log","log"],
                                                  "cuts": [np.s_[-5:]]}

# defining emulator paths
for system in AllData["Observables"]:
    for obs in AllData["Observables"][system]:
        AllData["Observables"][system][obs]["emulator"]["file"] = "emulators/"+system+obs+"-emulator.sav"

# validation
LEPvaldir = '/data/rjfgroup/rjf01/cameron.parker/runs/validation/LEP/QVir_Analysis/'
LHCvaldir = '/data/rjfgroup/rjf01/cameron.parker/runs/validation/LHC2760/QVir_Analysis/'

valData = copy.deepcopy(AllData)
valData["Design"] = ReadDesign(LHCvaldir+"parameters.txt")
valData["Observables"]["EpEm91"]["charged-xp"]["predictions"] = ReadPrediction(LEPvaldir+'charged-xp')
valData["Observables"]["EpEm91"]["pion-xp"]["predictions"] = ReadPrediction(LEPvaldir+'pion-xp')
valData["Observables"]["EpEm91"]["kaon-xp"]["predictions"] = ReadPrediction(LEPvaldir+'kaon-xp')
valData["Observables"]["EpEm91"]["proton-xp"]["predictions"] = ReadPrediction(LEPvaldir+'proton-xp')
valData["Observables"]["EpEm91"]["jets"]["predictions"] = ReadPrediction(LEPvaldir+'jet')


valData["Observables"]["PrPr2760"]["charged-pT"]["predictions"] = ReadPrediction(LHCvaldir+'HadronSpectraPrediction')
valData["Observables"]["PrPr2760"]["pion-pT"]["predictions"] = ReadPrediction(LHCvaldir+'PionSpectraPrediction')
valData["Observables"]["PrPr2760"]["kaon-pT"]["predictions"] = ReadPrediction(LHCvaldir+'KaonSpectraPrediction')
valData["Observables"]["PrPr2760"]["proton-pT"]["predictions"] = ReadPrediction(LHCvaldir+'ProtonSpectraPrediction')
valData["Observables"]["PrPr2760"]["jets-R2"]["predictions"] = ReadPrediction(LHCvaldir+'JetSpectraPredictionR2')
valData["Observables"]["PrPr2760"]["jets-R3"]["predictions"] = ReadPrediction(LHCvaldir+'JetSpectraPredictionR3')
valData["Observables"]["PrPr2760"]["jets-R4"]["predictions"] = ReadPrediction(LHCvaldir+'JetSpectraPredictionR4')
                                                  