import sys
import ROOT
import os
import numpy as np
from src.data_objects import AllData
from ctypes import *

def histToGraph(hist):
    n = hist.GetNbinsX()
    x = []
    xerr = []
    y = []
    yerr = []

    for i in range(n):
        thisy = hist.GetBinContent(i+1)
        thisyerr = hist.GetBinError(i+1)

        if thisy <= 0:
            continue
        
        if thisyerr > thisy:
            thisyerr = 0

        x.append(hist.GetBinCenter(i+1))
        xerr.append(hist.GetBinWidth(i+1)/2.)
        y.append(thisy)
        yerr.append(thisyerr)

    graph = ROOT.TGraphErrors(len(x),np.array(x),np.array(y),np.array(xerr),np.array(yerr))
    graph.SetTitle(hist.GetTitle())
    graph.SetName(hist.GetName())

    return graph

def cleanGraph(inGraph):
    n = inGraph.GetN()
    x = []
    xerr = []
    y = []
    yerr = []

    gmin = 1e30
    gmax = 0

    for i in range(n):
        thisx = c_double(0)
        thisy = c_double(0)
        inGraph.GetPoint(i,thisx,thisy)
        thisyerr = inGraph.GetErrorY(i)
        thisx = thisx.value
        thisy = thisy.value


        if thisy <= 0.0:
            thisy = 1e-30
        
        if thisyerr > thisy:
            thisyerr = thisy*0.99

        x.append(thisx)
        xerr.append(0.0)
        y.append(thisy)
        yerr.append(thisyerr)

        if thisy < gmin:
            gmin = abs(thisy - thisyerr)
        if thisy > gmax:
            gmax = thisy + thisyerr

    graph = inGraph.Clone() #ROOT.TGraphErrors(n,np.array(x),np.array(y),np.array(xerr),np.array(yerr))
    graph.SetTitle(inGraph.GetTitle())
    graph.SetName(inGraph.GetName())

    return graph, gmin, gmax

def getGraphs(mcDir):
    # directories
    graphList = []
    LEProot = mcDir + "LEP/points/0/totals.root"
    LHC2760root = mcDir + "LHC2760/points/0/root/totals.root"

    # root files
    LEPfile = ROOT.TFile(LEProot,"r")
    LHC2760file = ROOT.TFile(LHC2760root,"r")

    graphList.append(histToGraph(LEPfile.Get("hadrons")))
    graphList.append(histToGraph(LEPfile.Get("pions")))
    graphList.append(histToGraph(LEPfile.Get("kaons")))
    graphList.append(histToGraph(LEPfile.Get("protons")))
    graphList.append(histToGraph(LEPfile.Get("jets")))

    graphList.append(histToGraph(LHC2760file.Get("hadrons")))
    graphList.append(histToGraph(LHC2760file.Get("smooth pions")))
    graphList.append(histToGraph(LHC2760file.Get("smooth kaons")))
    graphList.append(histToGraph(LHC2760file.Get("smooth protons")))
    graphList.append(histToGraph(LHC2760file.Get("jet radius 0.2")))
    graphList.append(histToGraph(LHC2760file.Get("jet radius 0.3")))
    graphList.append(histToGraph(LHC2760file.Get("jet radius 0.4")))

    return graphList

def divideGraph(numerator, denominator):
    bins = int(denominator.GetN())

    xs = []
    ys = []
    xerrs = []
    yerrs = []
    for i in range(bins):
        x = c_double(0)
        y1 = c_double(0)
        y2 = c_double(0)
        numerator.GetPoint(i,x,y1)
        denominator.GetPoint(i,x,y2)
        yerr = numerator.GetErrorY(i)
        xerr = numerator.GetErrorX(i)
    
        if y2.value == 0:
            y2 = c_double(1.0)
            y1 = c_double(0)
            yerr = 0

        xs.append(float(x.value))
        ys.append(float(y1.value/y2.value))
        xerrs.append(float(xerr))
        yerrs.append(float(yerr/y2.value))

    return ROOT.TGraphErrors(bins,np.array(xs),np.array(ys),np.array(xerrs),np.array(yerrs))

def makePlot(MCs, data, plotvars, plotDir):
    # plot settings
    xlog = True if plotvars[2] == "log" else False
    ylog = True if plotvars[3] == "log" else False
    colors = [ROOT.kRed,ROOT.kBlue,ROOT.kBlue+3,ROOT.kAzure+10,ROOT.kBlue-10]
    title = plotvars[4]

    # Drawing main plot
    upperMG = ROOT.TMultiGraph()
    c = ROOT.TCanvas("c1","c1",1000,800)
    upper = ROOT.TPad("plot","plot",0,0.4,1,1)
    upper.SetBottomMargin(0)
    upper.Draw()
    upper.cd()

    # Data graph
    dataPlot, gmin, gmax = cleanGraph(data)
    dataPlot.SetMarkerStyle(ROOT.kFullDotLarge)
    dataPlot.SetMarkerColor(ROOT.kBlack)
    dataPlot.SetLineColor(ROOT.kBlack)
    dataPlot.SetTitle("data")
    upperMG.Add(dataPlot,"AP")
    upperMG.GetYaxis().SetLabelSize(0.04)
    upperMG.GetYaxis().SetTitle(plotvars[1])
    upperMG.GetHistogram().SetTitle(title)

    # prediction graph formatting
    for i, MC in enumerate(MCs):
        MCs[MC].SetLineColor(colors[i])
        MCs[MC].SetFillColorAlpha(colors[i], 0.35)
        MCs[MC].SetLineWidth(3)
        MCs[MC].SetName(MC)
        MCs[MC].SetTitle(MC)
        upperMG.Add(MCs[MC],"l3")

    # drawing
    if(ylog): 
        upper.SetLogy()
        upperMG.SetMinimum(gmin/2)
        upperMG.SetMaximum(gmax*2)
    if(xlog): upper.SetLogx()
    upperMG.Draw("AP")
    upper.BuildLegend()

    # ratio plots
    lowerMG = ROOT.TMultiGraph()

    # Data graph
    dataRatio = divideGraph(dataPlot,dataPlot)
    dataRatio.SetMarkerStyle(ROOT.kFullDotLarge)
    dataRatio.SetMarkerColor(ROOT.kBlack)
    dataRatio.SetLineColor(ROOT.kBlack)
    dataRatio.SetTitle(title)
    lowerMG.Add(dataRatio,"AP")
    lowerMG.GetYaxis().SetLabelSize(0.06)
    lowerMG.GetYaxis().SetTitleSize(0.06)
    lowerMG.GetXaxis().SetLabelSize(0.06)
    lowerMG.GetXaxis().SetTitleSize(0.06)
    lowerMG.GetYaxis().SetTitle("JETSCAPE/data")
    plotvars[0] = plotvars[0].replace('$', '')
    lowerMG.GetXaxis().SetTitle(plotvars[0])

    MCratios = []
    for i, MC in enumerate(MCs):
        thisRatio = divideGraph(MCs[MC],dataPlot)
        MCratios.append(thisRatio.Clone())
        MCratios[i].SetLineColor(colors[i])
        MCratios[i].SetFillColorAlpha(colors[i], 0.35)
        MCratios[i].SetLineWidth(3)
        lowerMG.Add(MCratios[i],"l3")

    # drawing ratio plot
    c.cd()
    lower = ROOT.TPad("plot","plot",0,0,1,0.4)
    lower.SetTopMargin(0)
    lower.SetBottomMargin(0.2)
    lower.Draw()
    lower.cd()
    if(xlog): lower.SetLogx()
    lowerMG.SetMaximum(2.1)
    lowerMG.SetMinimum(0.)
    lowerMG.Draw("AP")

    filename  = plotDir + title + ".png"
    c.Print(filename)
    c.Close()

#############################################################################################
# start of main

# getting 3 sets of input
defaultDir = "/data/rjfgroup/rjf01/cameron.parker/runs/default/"
tuneDir = sys.argv[1]
dataDir = "/data/rjfgroup/rjf01/cameron.parker/data/"

# making directory to put plots
plotDir = tuneDir + "plots/"
try:
    os.mkdir(plotDir)
except:
    print("Output dir exists, will be overwritten")

# lists for histograms
defaultList = getGraphs(defaultDir)
tuneList = getGraphs(tuneDir)

# getting data list
ALEPHfile = ROOT.TFile(dataDir+"ALEPH.root","r")
ALEPHjetfile = ROOT.TFile(dataDir+"ALEPH-jets.root","r")
LHC2760hadronfile = ROOT.TFile(dataDir+"HadronData.root","r")
LHC2760idfile = ROOT.TFile(dataDir+"LHC-ID-hads.root","r")
LHC2760jetfile = ROOT.TFile(dataDir+"JetData.root","r")
dataList = []

dataList.append(ALEPHfile.Get("Table 9").Get("Graph1D_y1")) # xp
dataList.append(ALEPHfile.Get("Table 25").Get("Graph1D_y1")) # pions
dataList.append(ALEPHfile.Get("Table 26").Get("Graph1D_y1")) # kaons
dataList.append(ALEPHfile.Get("Table 27").Get("Graph1D_y1")) # protons
dataList.append(ALEPHjetfile.Get("InclusiveJetEnergy").Get("Graph1D_y1")) # jets

dataList.append(LHC2760hadronfile.Get("Table 1").Get("Graph1D_y1")) # charged pt
dataList.append(LHC2760idfile.Get("Table 1").Get("Graph1D_y3")) # pions
dataList.append(LHC2760idfile.Get("Table 2").Get("Graph1D_y3")) # kaons
dataList.append(LHC2760idfile.Get("Table 3").Get("Graph1D_y3")) # protons
dataList.append(LHC2760jetfile.Get("Table 4").Get("Graph1D_y1")) # jets 0.2
dataList.append(LHC2760jetfile.Get("Table 4").Get("Graph1D_y2")) # jets 0.3
dataList.append(LHC2760jetfile.Get("Table 4").Get("Graph1D_y3")) # jets 0.4

# getting plot vars from existing data structure
plotVars = []
for system in AllData["Observables"]:
    for obs in AllData["Observables"][system]:
        plotVarsTemp = AllData["Observables"][system][obs]["plotvars"]
        plotVarsTemp.append(system+obs)
        plotVars.append(plotVarsTemp)

# making plots
for i in range(len(defaultList)):
    tempDict = {"default": defaultList[i],
                "tune": tuneList[i]
                }
    
    makePlot(tempDict, dataList[i], plotVars[i], plotDir)