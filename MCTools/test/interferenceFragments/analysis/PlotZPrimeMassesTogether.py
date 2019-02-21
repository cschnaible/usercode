import ROOT as R
import argparse,glob
import Plotter as Plotter
import tools as t
R.gROOT.SetBatch(True)

parser = argparse.ArgumentParser(description='Options for plotting mass distributions')
parser.add_argument('-in','--inname',default='',type=str,help='Identifier for input ROOT file')
parser.add_argument('-out','--outname',default='',type=str,help='Extra name to add to output')
parser.add_argument('-zp','--zprime',default='B-L',help='Which models to plot')
parser.add_argument('-d','--data',action='store_true',help='Draw data')
args = parser.parse_args()

MODEL = args.zprime
CHANNELS = ['EE','MuMu','LL']
DATE = args.inname
PDF = 'NNPDF30nlo'
#masses = [4000,4500,5000,5500,6000,6500,7000,7500,8000]
colors = {
        '4000':R.kRed-7,
        '4500':R.kRed+2,
        '5000':R.kMagenta-7,
        '5500':R.kMagenta+2,
        '6000':R.kBlue-7,
        '6500':R.kBlue+2,
        '7000':R.kGreen-3,
        '7500':R.kGreen+3,
        '8000':R.kOrange+1,
        '9000':R.kOrange+10,
        '10000':R.kViolet+10,
        '11000':R.kViolet+3,
        '12000':R.kSpring-1,
        '13000':R.kSpring-7,
        }
hpdfname = {
        'NNPDF30nlo':'_NNPDF30nlo',
        'CT10nlo':'_CT10nlo',
        'CT14nlo':'_CT14nlo',
        'CTEQ5L':'_CTEQ5L',
        }
pretty = {
        'MuMu':'#mu#mu',
        'EE':'ee',
        'LL':'ll',
        'ZPrime'+args.zprime:'Z\'_{'+args.zprime+'}',
        'DY':'Z^{0}/#gamma',
        'NNPDF30nlo':'NNPDF 3.0 (NLO)',
        'CT10nlo':'CT10 (NLO)',
        'CT14nlo':'CT14 (NLO)',
        'CTEQ5L':'CTEQ 5L (LO)',
        }

#massList = ['6000','7000','8000','9000','10000','11000','12000','13000']
#massList = ['6000','9000','10000','11000']
massList = ['6000','9000','12000']

for CHANNEL in CHANNELS:
    canvas = Plotter.Canvas(lumi='Z\'_{'+MODEL+'}#rightarrow'+pretty[CHANNEL],logy=True,extra='Private Work Simulation',ratioFactor=1./3)

    dyFile = R.TFile('root/ZprimeInterferenceHists_DY_'+PDF+'_'+DATE+'.root')
    dyHist = dyFile.Get('DYTo'+CHANNEL+hpdfname[PDF]).Clone()
    dyHist.Rebin(3)
    dyHist.SetDirectory(0)
    dyFile.Close()
    dyPlot = Plotter.Plot(dyHist,legName='Drell-Yan',legType='l',option='hist')
    zpPlots = {}
    fileList = glob.glob('root/ZprimeInterferenceHists_ZPrime'+MODEL+'_*_'+PDF+'_'+DATE+'.root')
    #for mass in masses:
    masses = []
    for zpFileName in fileList:
        mass = zpFileName.split('/')[1].split('.')[0].split('_')[2]
        if mass not in massList: continue
        masses.append(mass)
        #zpFile = R.TFile('root/ZprimeInterferenceHists_ZPrime'+MODEL+'_'+str(mass)+'_'+PDF+'_'+DATE+'.root')
        zpFile = R.TFile(zpFileName)
        # ZPrimeLRToEE_ResM6000_Int_NNPDF30nlo
        zpHist = zpFile.Get('ZPrime'+MODEL+'To'+CHANNEL+'_ResM'+str(mass)+'_Int'+hpdfname[PDF]).Clone()
        zpHist.Rebin(3)
        zpHist.SetDirectory(0)
        zpFile.Close()
        zpPlots[mass] = Plotter.Plot(zpHist,legName=str(mass)+' TeV',legType='l',option='hist')
    canvas.addMainPlot(dyPlot)
    dyPlot.SetLineWidth(1)
    dyPlot.SetLineColor(R.kBlack)
    for mass in masses: canvas.addMainPlot(zpPlots[mass])
    for mass in masses: 
        zpPlots[mass].SetLineColor(colors[mass])
        zpPlots[mass].SetLineWidth(1)
    #canvas.firstPlot.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
    #canvas.firstPlot.setTitles(X='mass [GeV]',Y='Events / 100 GeV')
    canvas.firstPlot.setTitles(X='mass [GeV]',Y='Events / 150 GeV')

    if args.data:
        datahist = R.TH1F('data','',180,0,9000)
        with open('data_Run2016_All_07Aug2017_list_sort_m600.txt') as f:
            lines = f.readlines()
            for line in lines:
                datahist.Fill(float(line))
        dataplot = Plotter.Plot(datahist,legName='2016 data',legType='pe',option='pe')
        canvas.addMainPlot(dataplot)

    canvas.makeLegend(pos='tr')
    canvas.legend.moveLegend(X=-0.1)
    canvas.legend.resizeHeight()
    canvas.setMaximum()
    for mass in masses:
        canvas.addRatioPlot(zpPlots[mass],dyPlot,color=colors[mass],ytit='S+B / B',xtit='mass [GeV]',option='hist',legName=str(mass)+' TeV',legType='pe',plusminus=1)
    if args.data: canvas.addRatioPlot(dataplot,dyPlot,option='pe')
    canvas.cleanup('plots/ZPrime'+MODEL+'To'+CHANNEL+'_'+PDF+('_'+args.outname if args.outname else '')+'.pdf')

