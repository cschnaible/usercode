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
parser.add_argument('-zp','--zprime',default='Q',type=str,help='Which model to plot')
parser.add_argument('-m','--mass',default='6000',type=str,help='Which Z-prime mass to plot')
parser.add_argument('-pdf','--pdf',default='NNPDF30nlo',type=str,help='Which PDF to plot')
args = parser.parse_args()

CHANNELS = ['MuMu','EE','LL']
CATEGORIES = ['all','bb','be','beee','ee']
#CATEGORIES = ['all','bb','beee']
#CATEGORIES = ['all','be','ee']
colors = {
        'all':R.kGreen+1,
        'bb':R.kOrange+1,
        'be':R.kRed,
        'beee':R.kBlue,
        'ee':R.kMagenta,
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
        'bb':'Barrel-Barrel',
        'be':'Barrel-Endcap + Endcap-Endcap',# this is confusing
        'ee':'Endcap-Endcap',
        'beee':'Barrel-Endcap',# this is confusing
        'all':'All categories'
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
PDF = args.pdf

for CHANNEL in CHANNELS:
    # Make PDF comparison plot for DY
    cDY = Plotter.Canvas(lumi=pretty['DY']+'#rightarrow'+pretty[CHANNEL],ratioFactor=1./3,extra='Private Work Simulation')
    dyHists = {CAT:{} for CAT in CATEGORIES}
    dyPlots = {CAT:{} for CAT in CATEGORIES}
    inFile = R.TFile('root/ZprimeInterferenceHists_DY_'+PDF+'_'+DATE+'.root')
    print inFile
    for CAT in CATEGORIES:
        print 'DYTo'+CHANNEL+hpdfname[PDF]+'_'+CAT
        dyHists[CAT] = inFile.Get('DYTo'+CHANNEL+hpdfname[PDF]+'_'+CAT).Clone()
        print dyHists[CAT]
        dyHists[CAT].SetDirectory(0)

        dyPlots[CAT] = Plotter.Plot(dyHists[CAT],legName=pretty[CAT],legType='l',option='hist')
        cDY.addMainPlot(dyPlots[CAT])
        dyPlots[CAT].SetLineColor(colors[CAT])
        dyPlots[CAT].SetLineWidth(1)
    inFile.Close()

    cDY.firstPlot.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
    cDY.makeLegend(pos='tr')
    cDY.legend.moveLegend(X=-0.2)
    cDY.legend.resizeHeight()
    cDY.setMaximum()
    cDY.mainPad.SetLogy(True)
    for CAT in CATEGORIES:
        if CAT=='all':continue
        cDY.addRatioPlot(dyPlots[CAT],dyPlots['all'],color=colors[CAT],legName=CAT+' / all',ytit='Ratio',xtit='mass [GeV]',center=0.5,drawLine=False)
    cDY.makeRatioLegend(pos='tr')
    cDY.ratLegend.moveLegend(X=-0.1)
    cDY.finishCanvas()
    cDY.save('plots/DYTo'+CHANNEL+'_category_comparison'+('_'+args.outname if args.outname else '')+'.pdf')
    cDY.deleteCanvas()

    # Make category comparison plot for ZPrimeB-L
    zpPlots = {CAT:{} for CAT in CATEGORIES}
    zpHists = {CAT:{} for CAT in CATEGORIES}
    cZP = Plotter.Canvas(lumi=pretty[MODEL]+'#rightarrow'+pretty[CHANNEL],ratioFactor=1./3,extra='Private Work Simulation')
    for CAT in CATEGORIES:
        inFile = R.TFile('root/ZprimeInterferenceHists_'+MODEL+'_'+MASS+'_'+PDF+'_'+DATE+'.root')
        hist = inFile.Get(MODEL+'To'+CHANNEL+'_ResM'+MASS+'_Int'+hpdfname[PDF]+'_'+CAT).Clone()
        hist.SetDirectory(0)
        inFile.Close()

        zpPlots[CAT] = Plotter.Plot(hist,legName=pretty[CAT],legType='l',option='hist')
        cZP.addMainPlot(zpPlots[CAT])
        zpPlots[CAT].SetLineColor(colors[CAT])
        zpPlots[CAT].SetLineWidth(1)

    cZP.firstPlot.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
    cZP.makeLegend(pos='tr')
    cZP.legend.moveLegend(X=-0.2)
    cZP.setMaximum()
    cZP.mainPad.SetLogy(True)
    for CAT in CATEGORIES:
        if CAT=='all':continue
        cZP.addRatioPlot(zpPlots[CAT],zpPlots['all'],color=colors[CAT],legName=CAT+' / all',ytit='Ratio',xtit='mass [GeV]',center=0.5,drawLine=False)
    cZP.makeRatioLegend(pos='tr')
    cZP.ratLegend.moveLegend(X=-0.1)
    cZP.finishCanvas()
    cZP.save('plots/'+MODEL+'To'+CHANNEL+'_M'+MASS+'_category_comparison'+('_'+args.outname if args.outname else '')+'.pdf')
    cZP.deleteCanvas()

    # Make category comparison plot for S+B/B
    cRat = Plotter.Canvas(lumi=pretty[MODEL]+'#rightarrow'+pretty[CHANNEL],ratioFactor=1./3,extra='Private Work Simulation')
    ratPlots = {CAT:{} for CAT in CATEGORIES}
    for CAT in CATEGORIES:
        zpFile = R.TFile('root/ZprimeInterferenceHists_'+MODEL+'_'+MASS+'_'+PDF+'_'+DATE+'.root')
        zpHist = zpFile.Get(MODEL+'To'+CHANNEL+'_ResM'+MASS+'_Int'+hpdfname[PDF]+'_'+CAT).Clone() 
        zpHist.SetDirectory(0)
        zpFile.Close()
        dyFile = R.TFile('root/ZprimeInterferenceHists_DY_'+PDF+'_'+DATE+'.root')
        dyHist = dyFile.Get('DYTo'+CHANNEL+hpdfname[PDF]+'_'+CAT).Clone()
        dyHist.SetDirectory(0)
        dyFile.Close()
        
        ratHist = zpHist.Clone(MODEL+'To'+CHANNEL+'_ResM'+MASS+'_DY_'+PDF+'_ratio_'+CAT)
        ratHist.Divide(dyHist)
        ratPlots[CAT] = Plotter.Plot(ratHist,legName=pretty[CAT],legType='l',option='hist')
        #ratGraph, r, erl, ery = tools.binomial_divide(zpHist.Clone(),dyHist.Clone(),confint=clopper_pearson_poisson_means,force_lt_1=False)
        #ratPlots[PDF] = Plotter.Plot(ratGraph,legName=pretty[PDF],legType='l',option='pe')
        cRat.addMainPlot(ratPlots[CAT])
        ratPlots[CAT].SetLineColor(colors[CAT])
        ratPlots[CAT].SetMarkerColor(colors[CAT])
        ratPlots[CAT].SetLineWidth(1)

    cRat.firstPlot.setTitles(X='mass [GeV]',Y='S+B / B')
    cRat.firstPlot.GetYaxis().SetRangeUser(0,2)
    cRat.firstPlot.GetXaxis().SetRangeUser(0,6000)
    cRat.makeLegend(pos='tl')
    cRat.legend.moveLegend(X=0.2)
    for CAT in CATEGORIES:
        if CAT=='all':continue
        cRat.addRatioPlot(ratPlots[CAT],ratPlots['all'],color=colors[CAT],legName=CAT+' / all',ytit='Ratio',xtit='mass [GeV]')
    cRat.makeRatioLegend(pos='tl')
    cRat.firstRatioPlot.GetXaxis().SetRangeUser(0,6000)
    cRat.finishCanvas()
    cRat.save('plots/Ratio_'+MODEL+'_M'+MASS+'_DY_'+CHANNEL+'_category_comparison'+('_'+args.outname if args.outname else '')+'.pdf')
    cRat.deleteCanvas()

    # Make combined plot of S+B and B plus ratio
    cComb = Plotter.Canvas(lumi=pretty[MODEL]+'#rightarrow'+pretty[CHANNEL],ratioFactor=1./3,extra='Private Work Simulation')
    for CAT in CATEGORIES:
        cComb.addMainPlot(zpPlots[CAT])
        cComb.addMainPlot(dyPlots[CAT],addToPlotList=False)
    for CAT in CATEGORIES:
        zpPlots[CAT].SetLineWidth(1)
        zpPlots[CAT].SetLineColor(colors[CAT])
        dyPlots[CAT].SetLineWidth(1)
        dyPlots[CAT].SetLineColor(colors[CAT])
        dyPlots[CAT].SetLineStyle(R.kDashed)
    cComb.firstPlot.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
    cComb.makeLegend(pos='tr')
    cComb.legend.moveLegend(X=-0.2)
    cComb.setMaximum()
    cComb.mainPad.SetLogy(True)
    for CAT in CATEGORIES:
        cComb.addRatioPlot(zpPlots[CAT],dyPlots[CAT],color=colors[CAT],ytit='S+B / B',xtit='mass [GeV]')
    cComb.cleanup('plots/'+MODEL+'To'+CHANNEL+'_M'+MASS+'_combined_cateogry_comparison'+('_'+args.outname if args.outname else '')+'.pdf')
