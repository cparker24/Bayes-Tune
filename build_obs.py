from src.readers import *
import ROOT
import numpy as np
import pandas as pd

buildObsPkl("/scratch/user/cameron.parker/projects/JETSCAPE/runs/LEPgluonmove","hadrons","hadrons",500)
buildObsPkl("/scratch/user/cameron.parker/projects/JETSCAPE/runs/LEPgluonmove","pions","pions",500)
buildObsPkl("/scratch/user/cameron.parker/projects/JETSCAPE/runs/LEPgluonmove","kaons","kaons",500)
buildObsPkl("/scratch/user/cameron.parker/projects/JETSCAPE/runs/LEPgluonmove","protons","protons",500)