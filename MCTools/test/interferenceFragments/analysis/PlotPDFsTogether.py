'''
Purpose of script is to compare 4 TeV and 6 TeV Z-prime B-L invariant mass
spectra generated with different PDFs
output
- Z'/DY mass spectra with interference with ratios to NNPDF3.0 (NLO)
- DY mass spectra with ratios to NNPDF3.0 (NLO)
- Ratios of Z' with interference to pure DY
'''
import ROOT as R
import argparse
import Plotter as Plotter
import glob 
R.gROOT.SetBatch(True)
parser = argparse.ArgumentParser(description='Options for plotting mass distributions')
parser.add_argument('-in','--inname',default='',type=str,help='Extra name to add to input ROOT file')
parser.add_argument('-out','--outname',default='',type=str,help='Extra name to add to output file')
parser.add_argument('-zp','--zprime',default='B-L',type=str,help='Which model to plot')
parser.add_argument('-m','--mass',default='6000',type=str,help='Which Z-prime mass to plot')
args = parser.parse_args()

CHANNELS = ['MuMu','EE','LL']
PDFs = ['NNPDF30nlo','CT10nlo','CT14nlo','CTEQ5L']
colors = {
        'NNPDF30nlo':R.kGreen+1,
        'CT10nlo':R.kOrange+1,
        'CT14nlo':R.kRed,
        'CTEQ5L':R.kBlue,
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
hpdfname = {
        'NNPDF30nlo':'_NNPDF30nlo',
        'CT10nlo':'_CT10nlo',
        'CT14nlo':'_CT14nlo',
        'CTEQ5L':'_CTEQ5L',
        }
DATE = args.inname
MODEL = 'ZPrime'+args.zprime
MASS = args.mass

for CHANNEL in CHANNELS:
    # Make PDF comparison plot for DY
    cDY = Plotter.Canvas(lumi=pretty['DY']+'#rightarrow'+pretty[CHANNEL],ratioFactor=1./3,extra='Private Work Simulation')
    dyPlots = {PDF:{} for PDF in PDFs}
    for PDF in PDFs:
        inFile = R.TFile('root/ZprimeInterferenceHists_DY_'+PDF+'_'+DATE+'.root')
        hist = inFile.Get('DYTo'+CHANNEL+hpdfname[PDF]).Clone()
        hist.SetDirectory(0)
        inFile.Close()

        dyPlots[PDF] = Plotter.Plot(hist,legName=pretty[PDF],legType='l',option='hist')
        cDY.addMainPlot(dyPlots[PDF])
        dyPlots[PDF].SetLineColor(colors[PDF])
        dyPlots[PDF].SetLineWidth(1)

    cDY.firstPlot.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
    cDY.makeLegend(pos='tr')
    cDY.legend.moveLegend(X=-0.2)
    cDY.legend.resizeHeight()
    cDY.setMaximum()
    cDY.mainPad.SetLogy(True)
    for PDF in PDFs:
        if PDF=='NNPDF30nlo':continue
        cDY.addRatioPlot(dyPlots[PDF],dyPlots['NNPDF30nlo'],color=colors[PDF],legName=PDF+' / NNPDF30nlo',ytit='Ratio',xtit='mass [GeV]',option='le')
    cDY.makeRatioLegend(pos='tr')
    cDY.ratLegend.moveLegend(X=-0.1)
    cDY.finishCanvas()
    cDY.save('plots/DYTo'+CHANNEL+'_comparison_PDF'+('_'+args.outname if args.outname else '')+'.pdf')
    cDY.deleteCanvas()

    # Make PDF comparison plot for ZPrimeB-L
    zpPlots = {PDF:{} for PDF in PDFs}
    cZP = Plotter.Canvas(lumi=pretty[MODEL]+'#rightarrow'+pretty[CHANNEL],ratioFactor=1./3,extra='Private Work Simulation')
    for PDF in PDFs:
        inFile = R.TFile('root/ZprimeInterferenceHists_'+MODEL+'_'+MASS+'_'+PDF+'_'+DATE+'.root')
        hist = inFile.Get(MODEL+'To'+CHANNEL+'_ResM'+MASS+'_Int'+hpdfname[PDF]).Clone()
        hist.SetDirectory(0)
        inFile.Close()

        zpPlots[PDF] = Plotter.Plot(hist,legName=pretty[PDF],legType='l',option='hist')
        cZP.addMainPlot(zpPlots[PDF])
        zpPlots[PDF].SetLineColor(colors[PDF])
        zpPlots[PDF].SetLineWidth(1)

    cZP.firstPlot.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
    cZP.makeLegend(pos='tr')
    cZP.legend.moveLegend(X=-0.2)
    cZP.setMaximum()
    cZP.mainPad.SetLogy(True)
    for PDF in PDFs:
        if PDF=='NNPDF30nlo':continue
        cZP.addRatioPlot(zpPlots[PDF],zpPlots['NNPDF30nlo'],color=colors[PDF],legName=PDF+' / NNPDF30nlo',ytit='Ratio',xtit='mass [GeV]',option='le')
    cZP.makeRatioLegend(pos='tr')
    cZP.ratLegend.moveLegend(X=-0.1)
    cZP.finishCanvas()
    cZP.save('plots/'+MODEL+'To'+CHANNEL+'_M'+MASS+'_PDF'+('_'+args.outname if args.outname else '')+'.pdf')
    cZP.deleteCanvas()

    # Make PDF comparison plot for S+B/B
    cRat = Plotter.Canvas(lumi=pretty[MODEL]+'#rightarrow'+pretty[CHANNEL],ratioFactor=1./3,extra='Private Work Simulation')
    ratPlots = {PDF:{} for PDF in PDFs}
    for PDF in PDFs:
        zpFile = R.TFile('root/ZprimeInterferenceHists_'+MODEL+'_'+MASS+'_'+PDF+'_'+DATE+'.root')
        zpHist = zpFile.Get(MODEL+'To'+CHANNEL+'_ResM'+MASS+'_Int'+hpdfname[PDF]).Clone() 
        zpHist.SetDirectory(0)
        zpFile.Close()
        dyFile = R.TFile('root/ZprimeInterferenceHists_DY_'+PDF+'_'+DATE+'.root')
        dyHist = dyFile.Get('DYTo'+CHANNEL+hpdfname[PDF]).Clone()
        dyHist.SetDirectory(0)
        dyFile.Close()
        
        ratHist = zpHist.Clone('ratio_'+MODEL+'To'+CHANNEL+'_DY_'+PDF)
        ratHist.Divide(dyHist)
        ratPlots[PDF] = Plotter.Plot(ratHist,legName=pretty[PDF],legType='l',option='hist')
        cRat.addMainPlot(ratPlots[PDF])
        ratPlots[PDF].SetLineColor(colors[PDF])
        ratPlots[PDF].SetLineWidth(1)

    cRat.firstPlot.setTitles(X='mass [GeV]',Y='S+B / B')
    cRat.firstPlot.GetYaxis().SetRangeUser(0,2)
    cRat.makeLegend(pos='tl')
    cRat.legend.moveLegend(X=0.2)
    for PDF in PDFs:
        if PDF=='NNPDF30nlo':continue
        cRat.addRatioPlot(ratPlots[PDF],ratPlots['NNPDF30nlo'],color=colors[PDF],legName=PDF+' / NNPDF30nlo',ytit='Ratio',xtit='mass [GeV]',option='le',plusminus=1.)
    cRat.makeRatioLegend(pos='tl')
    cRat.finishCanvas()
    cRat.save('plots/Ratio_'+MODEL+'_M'+MASS+'_DY_'+CHANNEL+'_PDF'+('_'+args.outname if args.outname else '')+'.pdf')
    cRat.deleteCanvas()

    # Make combined plot of S+B and B plus ratio
    cComb = Plotter.Canvas(lumi=pretty[MODEL]+'#rightarrow'+pretty[CHANNEL],ratioFactor=1./3,extra='Private Work Simulation')
    for PDF in PDFs:
        cComb.addMainPlot(zpPlots[PDF])
        cComb.addMainPlot(dyPlots[PDF],addToPlotList=False)
    for PDF in PDFs:
        zpPlots[PDF].SetLineWidth(1)
        zpPlots[PDF].SetLineColor(colors[PDF])
        dyPlots[PDF].SetLineWidth(1)
        dyPlots[PDF].SetLineColor(colors[PDF])
        dyPlots[PDF].SetLineStyle(R.kDashed)
    cComb.firstPlot.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
    cComb.makeLegend(pos='tr')
    cComb.legend.moveLegend(X=-0.2)
    cComb.setMaximum()
    cComb.mainPad.SetLogy(True)
    for PDF in PDFs:
        cComb.addRatioPlot(zpPlots[PDF],dyPlots[PDF],color=colors[PDF],ytit='S+B / B',xtit='mass [GeV]',option='le')
    cComb.cleanup('plots/'+MODEL+'To'+CHANNEL+'_M'+MASS+'_combined_PDF'+('_'+args.outname if args.outname else '')+'.pdf')
