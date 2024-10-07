from .readers import *
import copy

dataDir = '/data/rjfgroup/rjf01/cameron.parker/builds/Bayes-Tune/input/data/'
LEPdir = '/data/rjfgroup/rjf01/cameron.parker/runs/LEPdesign/QVir_Analysis/'
LHCdir = '/data/rjfgroup/rjf01/cameron.parker/runs/LHC2760design/QVir_Analysis/'
LHC13000dir = '/data/rjfgroup/rjf01/cameron.parker/runs/LHC13000design/QVir_Analysis/'

AllData = {}
AllData["Design"] = ReadDesign("/data/rjfgroup/rjf01/cameron.parker/builds/JETSCAPE/designs/totaldesign.txt")
AllData["Observables"] = {"EpEm91": {}, "PrPr2760": {}, "PrPr13000": {}}
AllData["Observables"]["EpEm91"]["charged-xp"] = {"data": ReadData(dataDir+'Data_ALEPH_EpEm91_charged-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'charged-xp'),
                                                  "emulator": {},
                                                  "plotvars": ["$x_{p}$","$dN/dx_{p}$","log","log"],
                                                  "cuts": [np.s_[-7:]]}
AllData["Observables"]["EpEm91"]["pion-xp"] = {"data": ReadData(dataDir+'Data_ALEPH_EpEm91_pion-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'pion-xp'),
                                                  "emulator": {},
                                                  "plotvars": ["$x_{p}$","$dN/dx_{p}$","log","log"],
                                                  "cuts": [np.s_[-2:]]}
AllData["Observables"]["EpEm91"]["kaon-xp"] = {"data": ReadData(dataDir+'Data_ALEPH_EpEm91_kaon-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'kaon-xp'),
                                                  "emulator": {},
                                                  "plotvars": ["$x_{p}$","$dN/dx_{p}$","log","log"],
                                                  "cuts": [np.s_[-2:]]}
AllData["Observables"]["EpEm91"]["proton-xp"] = {"data": ReadData(dataDir+'Data_ALEPH_EpEm91_proton-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'proton-xp'),
                                                  "emulator": {},
                                                  "plotvars": ["$x_{p}$","$dN/dx_{p}$","log","log"],
                                                  "cuts": [np.s_[-2:]]}
AllData["Observables"]["EpEm91"]["jets"] = {"data": ReadData(dataDir+'Data_ALEPH_EpEm91_inc-jets.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'jet'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$dN/dp_{T}$","linear","linear"],
                                                  "cuts": [np.s_[-2:]]}
AllData["Observables"]["EpEm91"]["mult"] = {"data": ReadData(dataDir+'Data_ALEPH_EpEm91_mult.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'mult'),
                                                  "emulator": {},
                                                  "plotvars": ["$N_{charged}$","$P(N_{charged})$","linear","linear"],
                                                  "cuts": [np.s_[-11:],np.s_[:2]]}


AllData["Observables"]["PrPr2760"]["charged-pT-soft"] = {"data": ReadData(dataDir+'Data_CMS_PrPr2760_charged-hads-soft.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'HadronSpectraPredictionSoft'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$d^2N/dp_{T}d\eta$","log","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["charged-pT-hard"] = {"data": ReadData(dataDir+'Data_CMS_PrPr2760_charged-hads-hard.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'HadronSpectraPredictionHard'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$d^2N/dp_{T}d\eta$","log","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["pion-pT-soft"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr2760_pions-soft.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'PionSpectraPredictionSoft'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$1/(N_{ev}*2\pi*p_T)d^2N/dp_{T}dy$","log","log"],
                                                  "cuts": [[np.s_[:-10]]]}
AllData["Observables"]["PrPr2760"]["pion-pT-hard"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr2760_pions-hard.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'PionSpectraPredictionHard'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$1/(N_{ev}*2\pi*p_T)d^2N/dp_{T}dy$","log","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["kaon-pT-soft"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr2760_kaons-soft.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'KaonSpectraPredictionSoft'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$1/(N_{ev}*2\pi*p_T)d^2N/dp_{T}dy$","log","log"],
                                                  "cuts": [np.s_[:-10]]}
AllData["Observables"]["PrPr2760"]["kaon-pT-hard"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr2760_kaons-hard.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'KaonSpectraPredictionHard'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$1/(N_{ev}*2\pi*p_T)d^2N/dp_{T}dy$","log","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["proton-pT-soft"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr2760_protons-soft.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'ProtonSpectraPredictionSoft'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$1/(N_{ev}*2\pi*p_T)d^2N/dp_{T}dy$","log","log"],
                                                  "cuts": [np.s_[:-10]]}
AllData["Observables"]["PrPr2760"]["proton-pT-hard"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr2760_protons-hard.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'ProtonSpectraPredictionHard'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$1/(N_{ev}*2\pi*p_T)d^2N/dp_{T}dy$","log","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["jets-R2"] = {"data": ReadData(dataDir+'Data_CMS_PrPr2760_jets-2.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'JetSpectraPredictionR2'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$d^2\sigma/dp_{T}d\eta$","linear","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["jets-R3"] = {"data": ReadData(dataDir+'Data_CMS_PrPr2760_jets-3.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'JetSpectraPredictionR3'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$d^2\sigma/dp_{T}d\eta$","linear","log"],
                                                  "cuts": []}
AllData["Observables"]["PrPr2760"]["jets-R4"] = {"data": ReadData(dataDir+'Data_CMS_PrPr2760_jets-4.dat'),
                                                  "predictions": ReadPrediction(LHCdir+'JetSpectraPredictionR4'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$d^2\sigma/dp_{T}d\eta$","linear","log"],
                                                  "cuts": []}

AllData["Observables"]["PrPr13000"]["pion-pT"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr13000_pions.dat'),
                                                  "predictions": ReadPrediction(LHC13000dir+'PionSpectraPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$1/N_{ev}d^2N/dp_{T}dy$","log","log"],
                                                  "cuts": [np.s_[:21]]}
AllData["Observables"]["PrPr13000"]["kaon-pT"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr13000_kaons.dat'),
                                                  "predictions": ReadPrediction(LHC13000dir+'KaonSpectraPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$1/N_{ev}d^2N/dp_{T}dy$","log","log"],
                                                  "cuts": [np.s_[:38]]}
AllData["Observables"]["PrPr13000"]["proton-pT"] = {"data": ReadData(dataDir+'Data_ALICE_PrPr13000_protons.dat'),
                                                  "predictions": ReadPrediction(LHC13000dir+'ProtonSpectraPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$1/N_{ev}d^2N/dp_{T}dy$","log","log"],
                                                  "cuts": [np.s_[29:39],np.s_[:14]]}
AllData["Observables"]["PrPr13000"]["low-y-jets"] = {"data": ReadData(dataDir+'Data_ATLAS_PrPr13000_low-y-jets.dat'),
                                                  "predictions": ReadPrediction(LHC13000dir+'LowYJetPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$d^2\sigma/dp_{T}dy$","log","log"],
                                                  "cuts": [np.s_[-5:]]}
AllData["Observables"]["PrPr13000"]["mid-y-jets"] = {"data": ReadData(dataDir+'Data_ATLAS_PrPr13000_mid-y-jets.dat'),
                                                  "predictions": ReadPrediction(LHC13000dir+'MidYJetPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$d^2\sigma/dp_{T}dy$","log","log"],
                                                  "cuts": [np.s_[-15:]]}
AllData["Observables"]["PrPr13000"]["high-y-jets"] = {"data": ReadData(dataDir+'Data_ATLAS_PrPr13000_high-y-jets.dat'),
                                                  "predictions": ReadPrediction(LHC13000dir+'HighYJetPrediction'),
                                                  "emulator": {},
                                                  "plotvars": ["$p_{T}$ [GeV]","$d^2\sigma/dp_{T}dy$","log","log"],
                                                  "cuts": [np.s_[-15:]]}

# defining emulator paths
for system in AllData["Observables"]:
    for obs in AllData["Observables"][system]:
        AllData["Observables"][system][obs]["emulator"]["file"] = "emulators/"+system+obs+"-emulator.sav"

# validation
LEPvaldir = '/data/rjfgroup/rjf01/cameron.parker/runs/validation/LEP/QVir_Analysis/'
LHCvaldir = '/data/rjfgroup/rjf01/cameron.parker/runs/validation/LHC2760/QVir_Analysis/'
LHC13000valdir = '/data/rjfgroup/rjf01/cameron.parker/runs/validation/LHC13000/QVir_Analysis/'

valData = copy.deepcopy(AllData)
valData["Design"] = ReadDesign("/data/rjfgroup/rjf01/cameron.parker/builds/JETSCAPE/designs/validation-design.txt")
valData["Observables"]["EpEm91"]["charged-xp"]["predictions"] = ReadPrediction(LEPvaldir+'charged-xp')
valData["Observables"]["EpEm91"]["pion-xp"]["predictions"] = ReadPrediction(LEPvaldir+'pion-xp')
valData["Observables"]["EpEm91"]["kaon-xp"]["predictions"] = ReadPrediction(LEPvaldir+'kaon-xp')
valData["Observables"]["EpEm91"]["proton-xp"]["predictions"] = ReadPrediction(LEPvaldir+'proton-xp')
valData["Observables"]["EpEm91"]["jets"]["predictions"] = ReadPrediction(LEPvaldir+'jet')
valData["Observables"]["EpEm91"]["mult"]["predictions"] = ReadPrediction(LEPvaldir+'mult')


valData["Observables"]["PrPr2760"]["charged-pT-soft"]["predictions"] = ReadPrediction(LHCvaldir+'HadronSpectraPredictionSoft')
valData["Observables"]["PrPr2760"]["charged-pT-hard"]["predictions"] = ReadPrediction(LHCvaldir+'HadronSpectraPredictionHard')
valData["Observables"]["PrPr2760"]["pion-pT-soft"]["predictions"] = ReadPrediction(LHCvaldir+'PionSpectraPredictionSoft')
valData["Observables"]["PrPr2760"]["pion-pT-hard"]["predictions"] = ReadPrediction(LHCvaldir+'PionSpectraPredictionHard')
valData["Observables"]["PrPr2760"]["kaon-pT-soft"]["predictions"] = ReadPrediction(LHCvaldir+'KaonSpectraPredictionSoft')
valData["Observables"]["PrPr2760"]["kaon-pT-hard"]["predictions"] = ReadPrediction(LHCvaldir+'KaonSpectraPredictionHard')
valData["Observables"]["PrPr2760"]["proton-pT-soft"]["predictions"] = ReadPrediction(LHCvaldir+'ProtonSpectraPredictionSoft')
valData["Observables"]["PrPr2760"]["proton-pT-hard"]["predictions"] = ReadPrediction(LHCvaldir+'ProtonSpectraPredictionHard')
valData["Observables"]["PrPr2760"]["jets-R2"]["predictions"] = ReadPrediction(LHCvaldir+'JetSpectraPredictionR2')
valData["Observables"]["PrPr2760"]["jets-R3"]["predictions"] = ReadPrediction(LHCvaldir+'JetSpectraPredictionR3')
valData["Observables"]["PrPr2760"]["jets-R4"]["predictions"] = ReadPrediction(LHCvaldir+'JetSpectraPredictionR4')

valData["Observables"]["PrPr13000"]["pion-pT"]["predictions"] = ReadPrediction(LHC13000valdir+'PionSpectraPrediction')
valData["Observables"]["PrPr13000"]["kaon-pT"]["predictions"] = ReadPrediction(LHC13000valdir+'KaonSpectraPrediction')
valData["Observables"]["PrPr13000"]["proton-pT"]["predictions"] = ReadPrediction(LHC13000valdir+'ProtonSpectraPrediction')
valData["Observables"]["PrPr13000"]["low-y-jets"]["predictions"] = ReadPrediction(LHC13000valdir+'LowYJetPrediction')
valData["Observables"]["PrPr13000"]["mid-y-jets"]["predictions"] = ReadPrediction(LHC13000valdir+'MidYJetPrediction')
valData["Observables"]["PrPr13000"]["high-y-jets"]["predictions"] = ReadPrediction(LHC13000valdir+'HighYJetPrediction')
                                                  