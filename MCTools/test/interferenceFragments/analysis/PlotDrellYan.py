import ROOT as R
import argparse
import Plotter as Plotter
R.gROOT.SetBatch(True)
parser = argparse.ArgumentParser(description='Options for plotting mass distributions')
parser.add_argument('-in','--inname',default='',type=str,help='Extra name to add to input')
parser.add_argument('-out','--outname',default='',type=str,help='Extra name to add to output')
parser.add_argument('-pdf','--pdf',default='NNPDF30nlo',type=str,help='Which PDF to plot')
args = parser.parse_args()

DATE = args.inname
PDF = args.pdf
CHANNELS = ['EE','MuMu','LL']

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
hpdfname = {
        'NNPDF30nlo':'_NNPDF30nlo',
        'CT10nlo':'_CT10nlo',
        'CT14nlo':'_CT14nlo',
        'CTEQ5L':'_CTEQ5L',
        }

dyFile = R.TFile('root/ZprimeInterferenceHists_DY_'+PDF+'_'+DATE+'.root')

for CHANNEL in CHANNELS:
    dyHist = dyFile.Get('DYTo'+CHANNEL+hpdfname[PDF]).Clone()
    dyHist.SetDirectory(0)
    # log scale
    canvLog = Plotter.Canvas(extra='Preliminary Work Simulation',lumi=pretty['DY']+'#rightarrow'+pretty[CHANNEL],logy=True)
    dyPlotLog = Plotter.Plot(dyHist,option='hist')
    canvLog.addMainPlot(dyPlotLog)
    dyPlotLog.SetLineWidth(1)
    dyPlotLog.SetLineColor(R.kBlack)
    dyPlotLog.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
    canvLog.cleanup('plots/drellyan_'+CHANNEL+'_'+PDF+'_log_'+args.outname+'.pdf')

    # linear scale
    canvLin = Plotter.Canvas(extra='Preliminary Work Simulation',lumi=pretty['DY']+'#rightarrow'+pretty[CHANNEL])
    dyPlotLin = Plotter.Plot(dyHist,option='hist')
    canvLin.addMainPlot(dyPlotLin)
    dyPlotLin.SetLineWidth(1)
    dyPlotLin.SetLineColor(R.kBlack)
    dyPlotLin.GetYaxis().SetRangeUser(0,100)
    #dyPlotLin.GetXaxis().SetRangeUser(0000,9000)
    dyPlotLin.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
    canvLin.cleanup('plots/drellyan_'+CHANNEL+'_'+PDF+'_lin_'+args.outname+'.pdf')
dyFile.Close()
