import ROOT as R
import argparse
import Plotter as Plotter
R.gROOT.SetBatch(True)
parser = argparse.ArgumentParser(description='Options for plotting mass distributions')
parser.add_argument('-in','--inname',default='',type=str,help='Extra name to add to input')
parser.add_argument('-out','--outname',default='',type=str,help='Extra name to add to output')
parser.add_argument('-zp','--zprime',action='append',help='Which models to plot')
parser.add_argument('-pdf','--pdf',default='NNPDF30nlo',type=str,help='Which PDF to plot')
parser.add_argument('-m','--mass',default='6000',type=str,help='Which mass to plot')
args = parser.parse_args()

if args.zprime==['all']:
    MODELS = ['Q','PSI','T3L','SSM','B-L','LR','R','Y']
else:
    MODELS = [model for model in args.zprime]
print args.zprime
print MODELS 
colors = {
        'Q':R.kCyan+4,
        'SSM':R.kOrange+1,
        'T3L':R.kRed,

        'B-L':R.kBlue,
        'LR':R.kGreen+1,
        'R':R.kMagenta+1,
        'Y':R.kRed+3,

        'PSI':R.kViolet+5,
        'Chi':R.kYellow-3,
        'Eta':R.kCyan+2,
        'N':R.kGray,
        'I':R.kAzure+5,
        'SQ':R.kCyan,
        }
DATE = args.inname
MASS = args.mass
PDF = args.pdf
CHANNELS = ['EE','MuMu','LL']
hpdfname = {
        'NNPDF30nlo':'_NNPDF30nlo',
        'CT10nlo':'_CT10nlo',
        'CT14nlo':'_CT14nlo',
        'CTEQ5L':'_CTEQ5L',
        }
def get_pretty(name):
    pretty = {
            'MuMu':'#mu#mu',
            'EE':'ee',
            'LL':'ll',
            'DY':'Z^{0}/#gamma',
            'NNPDF30nlo':'NNPDF 3.0 (NLO)',
            'CT10nlo':'CT10 (NLO)',
            'CT14nlo':'CT14 (NLO)',
            'CTEQ5L':'CTEQ 5L (LO)',
            }
    if 'ZPrime' in name:
        return 'Z\'_{'+name.strip('ZPrime')+'}'
    else:
        return pretty[name]

for CHANNEL in CHANNELS:
    canvas = Plotter.Canvas(extra='Private Work Simulation',ratioFactor=1./3,logy=True)

    # Plot Z-primes with DY and ratio
    dyFile = R.TFile('root/ZprimeInterferenceHists_DY_'+PDF+'_'+DATE+'.root')
    dyHist = dyFile.Get('DYTo'+CHANNEL+hpdfname[PDF]).Clone()
    dyHist.SetDirectory(0)
    dyFile.Close()
    dyPlot = Plotter.Plot(dyHist,legName='Drell-Yan',legType='l',option='hist')
    zpPlots = {model:{} for model in MODELS}
    for MODEL in MODELS:
        zpFile = R.TFile('root/ZprimeInterferenceHists_ZPrime'+MODEL+'_'+MASS+'_'+PDF+'_'+DATE+'.root')
        # ZPrimeLRToEE_ResM6000_Int_NNPDF30nlo
        zpHist = zpFile.Get('ZPrime'+MODEL+'To'+CHANNEL+'_ResM'+MASS+'_Int'+hpdfname[PDF]).Clone()
        zpHist.SetDirectory(0)
        zpFile.Close()
        zpPlots[MODEL] = Plotter.Plot(zpHist,legName=get_pretty('ZPrime'+MODEL),legType='l',option='hist')
    canvas.addMainPlot(dyPlot)
    dyPlot.SetLineWidth(1)
    dyPlot.SetLineColor(R.kBlack)
    for MODEL in MODELS: canvas.addMainPlot(zpPlots[MODEL])
    for MODEL in MODELS: 
        zpPlots[MODEL].SetLineColor(colors[MODEL])
        zpPlots[MODEL].SetLineWidth(1)
    canvas.firstPlot.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
    canvas.makeLegend(pos='tr')
    canvas.legend.moveLegend(X=-0.1)
    canvas.legend.resizeHeight()
    canvas.setMaximum()
    for MODEL in MODELS:
        canvas.addRatioPlot(zpPlots[MODEL],dyPlot,color=colors[MODEL],ytit='S+B / B',xtit='mass [GeV]',option='pe',legName=get_pretty('ZPrime'+MODEL),legType='pe')
    modellist = ''
    for MODEL in MODELS: modellist+='_'+MODEL
    canvas.cleanup('plots/ZPrimeTo'+CHANNEL+modellist+'_'+MASS+'_'+PDF+('_'+args.outname if args.outname else '')+'.pdf')

    # Plot Ratios only
    canvRat = Plotter.Canvas(extra='Private Work Simulation',lumi='')
    ratPlots = {}
    for MODEL in MODELS:
        zpFile = R.TFile('root/ZprimeInterferenceHists_ZPrime'+MODEL+'_'+MASS+'_'+PDF+'_'+DATE+'.root')
        ratHist = zpFile.Get('ZPrime'+MODEL+'To'+CHANNEL+'_ResM'+MASS+'_Int'+hpdfname[PDF]).Clone('num_'+MODEL+'_'+CHANNEL)
        ratHist.SetDirectory(0)
        zpFile.Close()
        ratHist.Divide(dyHist)
        print ratHist
        ratPlots[MODEL] = Plotter.Plot(ratHist,legName=get_pretty('ZPrime'+MODEL),legType='l',option='hist')
        canvRat.addMainPlot(ratPlots[MODEL])
        ratPlots[MODEL].SetLineWidth(1)
        ratPlots[MODEL].SetLineColor(colors[MODEL])
    canvRat.firstPlot.setTitles(X='mass [GeV]',Y='S+B / B')
    canvRat.makeLegend(pos='tl')
    canvRat.firstPlot.GetYaxis().SetRangeUser(0,2)
    canvRat.cleanup('plots/ratio_ZPrimeTo'+CHANNEL+modellist+'_'+MASS+'_'+PDF+('_'+args.outname if args.outname else '')+'.pdf')
