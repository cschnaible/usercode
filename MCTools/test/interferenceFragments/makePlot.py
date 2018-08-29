import ROOT as R
import os
import Plotter
R.gROOT.SetBatch(True)

LUMI = 36300.

#ZpIntFileTmp = 'crab/crab_{MODEL}To{CHAN}_ResM{RES}_M{MLOW}To{MHIGH}_Interference_13TeV-pythia8/results/{MODEL}To{CHAN}_ResM{RES}_M{MLOW}To{MHIGH}_Interference_13TeV-pythia8_cff_1.root'
#ZpFileTmp = 'crab/crab_{MODEL}To{CHAN}_ResM{RES}_13TeV-pythia8/results/{MODEL}To{CHAN}_ResM{RES}_13TeV-pythia8_cff_1.root'
#DYFileTmp = 'crab/crab_DYTo{CHAN}_M{MLOW}To{MHIGH}_13TeV-pythia8/results/DYTo{CHAN}_M{MLOW}To{MHIGH}_13TeV-pythia8_cff_1.root'

# Using EE files for now for everything since the MuMu ones didn't have correct configuration
# Doesn't actually matter either since all the couplings are flavor independent
ZpIntFileTmp = 'crab/crab_{MODEL}ToEE_ResM{RES}_M{MLOW}To{MHIGH}_Interference_13TeV-pythia8/results/{MODEL}ToEE_ResM{RES}_M{MLOW}To{MHIGH}_Interference_13TeV-pythia8_cff_1.root'
ZpFileTmp = 'crab/crab_{MODEL}ToEE_ResM{RES}_13TeV-pythia8/results/{MODEL}ToEE_ResM{RES}_13TeV-pythia8_cff_1.root'
DYFileTmp = 'crab/crab_DYToEE_M{MLOW}To{MHIGH}_13TeV-pythia8/results/DYToEE_M{MLOW}To{MHIGH}_13TeV-pythia8_cff_1.root'
CHANNELS = ['EE','MuMu','LL']
#RESMASSES = [4000,6000]
RESMASSES = [4000,4500,5000,5500,6000,6500,7000,7500,8000]
MASSBINS = ['120','200','400','800','1400','2300','3500','4500','6000','Inf']
#MODELS = ["ZPrimeQ","ZPrimeSSM","ZPrimePSI","ZPrimeN","ZPrimeSQ","ZPrimeI","ZPrimeEta","ZPrimeChi","ZPrimeR","ZPrimeB-L","ZPrimeLR","ZPrimeY","ZPrimeT3L"]
MODELS = ["ZPrimeQ","ZPrimeSSM","ZPrimeSQ","ZPrimeR","ZPrimeB-L","ZPrimeLR","ZPrimeY","ZPrimeT3L"]

outFile = R.TFile.Open('test.root','recreate')

def sigma(chan):
    if chan=='EE':
        return '0.01*bosonP4.mass*((abs(decay1P4.eta)=<1.2 && abs(decay2P4.eta)=<1.2)*(sqrt((pow(10.3,2)/bosonP4.mass)+pow(10.0/bosonP4.mass,2)+pow(0.87,2))+5.6e-5*bosonP4.mass)+(abs(decay1P4.eta)>1.2 || abs(decay2P4.eta)>1.2)*sqrt((pow(14.5,2)/bosonP4.mass)+pow(10.0/bosonP4.mass,2)+pow(1.49,2)))'
    if chan=='MuMu':
        return 'bosonP4.mass*((abs(decay1P4.eta)=<1.2 && abs(decay2P4.eta)=<1.2)*(0.00701+3.32e-5*bosonP4.mass-1.29e-8*pow(bosonP4.mass,2)+2.73e-12*pow(bosonP4.mass,3)-2.05e-16*pow(bosonP4.mass,4))+(abs(decay1P4.eta)>1.2 || abs(decay2P4.eta)>1.2)*(0.0142+3.75e-5*bosonP4.mass-1.52e-8*pow(bosonP4.mass,2)+3.44e-12*pow(bosonP4.mass,3)-2.85e-16*pow(bosonP4.mass,4)))'
    if chan=='LL': return '0.'

def eff(chan):
    if chan=='EE':
        return '((abs(decay1P4.eta)=<1.2 && abs(decay2P4.eta)=<1.2)*(0.6484-500.5/(bosonP4.mass+362.3)+6.863e4/(pow(bosonP4.mass,2)+1.209e5)) + (abs(decay1P4.eta)>1.2 || abs(decay2P4.eta)>1.2)*(-0.03434+739/(bosonP4.mass+1260.)-9.172e4/(pow(bosonP4.mass,2)+7.39e4)+1.412e7/(pow(bosonP4.mass,3)+2.185e7)))'
    if chan=='MuMu':
        return '((abs(decay1P4.eta)=<1.2 && abs(decay2P4.eta)=<1.2)*((bosonP4.mass>=120 && bosonP4.mass<600)*(2.129-0.1268*exp(-1*(bosonP4.mass-119.2)/22.35)-2.386*pow(bosonP4.mass,-0.03619)) + (bosonP4.mass>=600)*(2.891-(2.291e4/(bosonP4.mass+8294.)-0.0001247*bosonP4.mass))) + (abs(decay1P4.eta)>1.2 || abs(decay2P4.eta)>1.2)*((bosonP4.mass>=120 && bosonP4.mass<450)*(13.56-6.672*exp((bosonP4.mass+4.879e6)/7.233e6)-826.0*pow(bosonP4.mass,-1.567)) + (bosonP4.mass>=450)*(0.2529+0.06511*pow(bosonP4.mass,0.8755)*exp(-1*(bosonP4.mass+4601)/1147.0))))'

    if chan=='LL': return '1.'



def makeHist(i,hname,fileName):
        print 'ls',fileName
        f = R.TFile(fileName)
        if i==0:
            h = R.TH1F(hname,'',140,0,7000)
            h.Sumw2()
        else:
            h = R.gROOT.FindObject(hname).Clone(hname)
        pdfTree = f.Get('pdfTree')
        # Resolution smearing
        # rndm is a random value generated between 0 and 1.. pretty convienient for smearing
        pdfTree.SetAlias('z','sin(2*pi*rndm)*sqrt(-2*log(rndm))')
        ISFIRST = '' if i==0 else '+'
        draw = 'bosonP4.mass + {SIGMA}*z >> {ISFIRST}{HISTNAME}'.format(ISFIRST=ISFIRST,SIGMA=sigma(CHAN),HISTNAME=hname)
        NEVENTS = float(pdfTree.GetEntries())
        XS = pdfTree.GetUserInfo().FindObject('crossSec').GetVal()
        weight = '{EFF}*{XS}*{LUMI}/{NEVENTS}'.format(EFF=eff(CHAN),XS=XS,LUMI=LUMI,NEVENTS=NEVENTS)
        option = 'hist'
        print draw,weight
        pdfTree.Draw(draw,weight,option)
        R.gROOT.FindObject(hname).SetDirectory(0)
        f.Close()
        return R.gROOT.FindObject(hname)

for CHAN in CHANNELS:
    # Do DY histograms
    dyname = 'DYTo'+CHAN
    for i in range(0,len(MASSBINS)-1):
        #fileName = DYFileTmp.format(CHAN=CHAN,MLOW=MASSBINS[i],MHIGH=MASSBINS[i+1])
        fileName = DYFileTmp.format(MLOW=MASSBINS[i],MHIGH=MASSBINS[i+1])
        h = makeHist(i,dyname,fileName)
    outFile.cd()
    R.gROOT.FindObject(dyname).Write()
    # Do interference histograms
    for RES in RESMASSES:
        for MODEL in MODELS:
            for interference in [True,False]:
                if interference:
                    hname = MODEL+'To'+CHAN+'_M'+str(RES)+'_Int'
                    for i in range(0,len(MASSBINS)-1):
                        #fileName = ZpIntFileTmp.format(MODEL=MODEL,RES=RES,CHAN=CHAN,MLOW=MASSBINS[i],MHIGH=MASSBINS[i+1])
                        fileName = ZpIntFileTmp.format(MODEL=MODEL,RES=RES,MLOW=MASSBINS[i],MHIGH=MASSBINS[i+1])
                        h = makeHist(i,hname,fileName)
                    outFile.cd()
                    R.gROOT.FindObject(hname).Write()
                else:
                    hname = MODEL+'To'+CHAN+'_M'+str(RES)
                    fileName = ZpFileTmp.format(MODEL=MODEL,RES=RES)
                    #fileName = ZpFileTmp.format(MODEL=MODEL,RES=RES,CHAN=CHAN)
                    h = makeHist(0,hname,fileName)
                    outFile.cd()
                    R.gROOT.FindObject(hname).Write()
            # Draw stuff together here and make it pretty
            c = Plotter.Canvas(lumi='36.3 fb^{-1} (13 TeV)',ratioFactor=1./3,extra='Private Work Simulation')
            zPIntPlot = Plotter.Plot(R.gROOT.FindObject(MODEL+'To'+CHAN+'_M'+str(RES)+'_Int'),legName='Drell-Yan x Z\'_{{{MODEL}}}'.format(MODEL=MODEL[6:]),legType='l',option='hist')
            dyPlot = Plotter.Plot(R.gROOT.FindObject(dyname),legName='Drell-Yan',legType='l',option='hist')
            zPPlot = Plotter.Plot(R.gROOT.FindObject(MODEL+'To'+CHAN+'_M'+str(RES)),legName='Pure Z\'_{{{MODEL}}}'.format(MODEL=MODEL[6:]),legType='l',option='hist')
            c.addMainPlot(zPIntPlot)
            c.addMainPlot(dyPlot)
            c.addMainPlot(zPPlot)
            c.firstPlot.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
            hmax = dyPlot.GetMaximum()*1.1
            c.firstPlot.GetYaxis().SetRangeUser(1e-6,hmax)
            c.makeLegend(pos='tr')
            c.legend.moveLegend(X=-0.2)
            c.setMaximum()
            dyPlot.SetLineColor(R.kBlack)
            zPIntPlot.SetLineColor(R.kRed)
            zPPlot.SetLineColor(R.kOrange)
            c.mainPad.SetLogy(True)
            c.addRatioPlot(zPIntPlot,dyPlot,color=R.kRed,ytit='S+B / B',xtit='mass [GeV]',option='pe')
            c.finishCanvas()
            outFile.cd()
            c.Write(MODEL+'To'+CHAN+'_M'+str(RES)+'_all')
        

