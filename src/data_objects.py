from readers import *

LEPdir = '/scratch/user/cameron.parker/projects/JETSCAPE/runs/LEPgluonmove/QVir_Analysis/'

AllData = {}
AllData["Design"] = ReadDesign(LEPdirr+"parameters.txt")
AllData["Observables"] = {"EpEm91": {}}
AllData["Observables"]["EpEm91"]["charged-xp"] = {"data": ReadData('/scratch/user/cameron.parker/projects/STAT/input/vac-data/Data_ALEPH_EpEm91_charged-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'charged-xp.dat')}
AllData["Observables"]["EpEm91"]["pion-xp"] = {"data": ReadData('/scratch/user/cameron.parker/projects/STAT/input/vac-data/Data_ALEPH_EpEm91_pion-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'pion-xp.dat')}
AllData["Observables"]["EpEm91"]["kaon-xp"] = {"data": ReadData('/scratch/user/cameron.parker/projects/STAT/input/vac-data/Data_ALEPH_EpEm91_kaon-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'kaon-xp.dat')}
AllData["Observables"]["EpEm91"]["proton-xp"] = {"data": ReadData('/scratch/user/cameron.parker/projects/STAT/input/vac-data/Data_ALEPH_EpEm91_proton-xp.dat'),
                                                  "predictions": ReadPrediction(LEPdir+'proton-xp.dat')}