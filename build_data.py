from src.readers import *

datafiles= [
    "/scratch/user/cameron.parker/projects/STAT/input/vac-data/Data_ALEPH_EpEm91_charged-xp.dat",
    "/scratch/user/cameron.parker/projects/STAT/input/vac-data/Data_ALEPH_EpEm91_pion-xp.dat",
    "/scratch/user/cameron.parker/projects/STAT/input/vac-data/Data_ALEPH_EpEm91_kaon-xp.dat",
    "/scratch/user/cameron.parker/projects/STAT/input/vac-data/Data_ALEPH_EpEm91_proton-xp.dat"
]

TestData = [ReadData(datafile) for datafile in datafiles]
buildDataPkl(TestData)