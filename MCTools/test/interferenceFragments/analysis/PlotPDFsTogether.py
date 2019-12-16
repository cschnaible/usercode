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
parser.add_argument('-r','--rebin',default=1,type=int,help='Rebin histograms')
args = parser.parse_args()
factor = 10
PDFstoCompare = {\
        'NNPDF':['NNPDF30nlo','NNPDF31nlo_TuneCP3','NNPDF31nnlo_PR_TuneCP5'],
        'CT':['NNPDF30nlo','CT10nlo','CT14nlo'],
        }
colors = {
        'NNPDF30nlo':R.kGreen+1,
        'NNPDF31nnlo_PR_TuneCP5':R.kBlack,
        'NNPDF31nlo_TuneCP3':R.kBlue,
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
        'NNPDF30nlo':'NNPDF3.0 (NLO)',
        'NNPDF31nlo_TuneCP3':'NNPDF3.1 (NLO)',
        'NNPDF31nnlo_PR_TuneCP5':'NNPDF3.1 (NNLO) PR',
        'CT10nlo':'CT10 (NLO)',
        'CT14nlo':'CT14 (NLO)',
        'CTEQ5L':'CTEQ 5L (LO)',
        }
hpdfname = {
        'NNPDF30nlo':'_NNPDF30nlo',
        'NNPDF31nnlo_PR_TuneCP5':'_NNPDF31nnlo_PR_TuneCP5',
        'NNPDF31nlo_TuneCP3':'_NNPDF31nlo_TuneCP3',
        'CT10nlo':'_CT10nlo',
        'CT14nlo':'_CT14nlo',
        'CTEQ5L':'_CTEQ5L',
        }
axes = {
        'mass':{'x':'mass [GeV]','y':'Events / bin'},
        'rapidity':{'x':'rapidity','y':'Events / bin'},
        'bosonPz':{'x':'p_{z} [GeV]','y':'Events / bin'},
        }
ranges = {
        'mass':[0,9000],
        'rapidity':[-3,3],
        'bosonPz':[0,5000],
        }
rootname = {
        'DY':{
            'NNPDF30nlo':'20190311',
            'NNPDF31nlo_TuneCP3':'20190311',
            'NNPDF31nnlo_PR_TuneCP5':'20190311',
            'CT10nlo':'20190311',
            'CT14nlo':'20190311',
            },
        'ZPrimeQ':{
            'NNPDF30nlo':'20190311',
            'NNPDF31nlo_TuneCP3':'20190311',
            'NNPDF31nnlo_PR_TuneCP5':'20190311',
            'CT10nlo':'20190311',
            'CT14nlo':'20190311',
            },
        }

DATE = args.inname
MODEL = 'ZPrime'+args.zprime
MASS = args.mass
REBIN = args.rebin
CHANNEL = 'LL'
QUANTITIES = ['rapidity']#,'mass','bosonPz']
CUTS = ['low','mid','high','all']

for CUT in CUTS:
    for QUANTITY in QUANTITIES:
        if QUANTITY=='mass' and CUT in ['high','mid','low']: continue
        for PDFs in PDFstoCompare:
            # Make PDF comparison plot for DY
            cDY = Plotter.Canvas(lumi=pretty['DY']+'#rightarrow'+pretty[CHANNEL],ratioFactor=1./3,extra='Private Work Simulation')
            dyPlots = {PDF:{} for PDF in PDFstoCompare[PDFs]}
            for PDF in PDFstoCompare[PDFs]:
                inFile = R.TFile('root/ZprimeInterferenceHists_DY_'+PDF+'_'+rootname['DY'][PDF]+'.root')
                hist = inFile.Get('DYTo'+CHANNEL+hpdfname[PDF]+'_'+QUANTITY+'_'+CUT).Clone()
                hist.SetDirectory(0)
                hist.Rebin(REBIN)
                hist.GetXaxis().SetRangeUser(ranges[QUANTITY][0],ranges[QUANTITY][1])
                inFile.Close()

                dyPlots[PDF] = Plotter.Plot(hist,legName=pretty[PDF],legType='l',option='hist')
                cDY.addMainPlot(dyPlots[PDF])
                dyPlots[PDF].SetLineColor(colors[PDF])
                dyPlots[PDF].SetLineWidth(1)

            cDY.firstPlot.setTitles(X=axes[QUANTITY]['x'],Y=axes[QUANTITY]['y'])
            cDY.makeLegend(pos='tr')
            cDY.legend.moveLegend(X=-0.2)
            cDY.legend.resizeHeight()
            cDY.setMaximum(factor)
            cDY.mainPad.SetLogy(True)
            for PDF in PDFstoCompare[PDFs]:
                if PDF=='NNPDF30nlo':continue
                cDY.addRatioPlot(dyPlots[PDF],dyPlots['NNPDF30nlo'],color=colors[PDF],legName=PDF+' / NNPDF30nlo',ytit='Ratio',xtit=axes[QUANTITY]['x'],plusminus=1.)
            cDY.makeRatioLegend(pos='tr')
            cDY.ratLegend.moveLegend(X=-0.1)
            cDY.finishCanvas()
            cDY.save('plots/DYTo'+CHANNEL+'_comparison_'+QUANTITY+'_'+CUT+'_'+PDFs+('_'+args.outname if args.outname else '')+'.pdf')
            cDY.deleteCanvas()

            # Make PDF comparison plot for ZPrime
            zpPlots = {PDF:{} for PDF in PDFstoCompare[PDFs]}
            cZP = Plotter.Canvas(lumi=pretty[MODEL]+'#rightarrow'+pretty[CHANNEL],ratioFactor=1./3,extra='Private Work Simulation')
            for PDF in PDFstoCompare[PDFs]:
                filename = 'root/ZprimeInterferenceHists_'+MODEL+'_'+MASS+'_'+PDF+'_'+rootname[MODEL][PDF]+'.root'
                print filename
                inFile = R.TFile(filename)
                hname = MODEL+'To'+CHANNEL+('_M' if PDF=='NNPDF30nlo' else '_M')+MASS+'_Int'+hpdfname[PDF]
                print hname
                hist = inFile.Get(hname+'_'+QUANTITY+'_'+CUT).Clone()
                hist.SetDirectory(0)
                hist.Rebin(REBIN)
                hist.GetXaxis().SetRangeUser(ranges[QUANTITY][0],ranges[QUANTITY][1])
                inFile.Close()

                zpPlots[PDF] = Plotter.Plot(hist,legName=pretty[PDF],legType='l',option='hist')
                cZP.addMainPlot(zpPlots[PDF])
                zpPlots[PDF].SetLineColor(colors[PDF])
                zpPlots[PDF].SetLineWidth(1)

            cZP.firstPlot.setTitles(X=axes[QUANTITY]['x'],Y=axes[QUANTITY]['y'])
            cZP.makeLegend(pos='tr')
            cZP.legend.moveLegend(X=-0.2)
            cZP.setMaximum(factor)
            cZP.mainPad.SetLogy(True)
            for PDF in PDFstoCompare[PDFs]:
                if PDF=='NNPDF30nlo':continue
                cZP.addRatioPlot(zpPlots[PDF],zpPlots['NNPDF30nlo'],color=colors[PDF],legName=PDF+' / NNPDF30nlo',ytit='Ratio',xtit=axes[QUANTITY]['x'],plusminus=1.)
            cZP.makeRatioLegend(pos='tr')
            cZP.ratLegend.moveLegend(X=-0.1)
            cZP.finishCanvas()
            cZP.save('plots/'+MODEL+'To'+CHANNEL+'_M'+MASS+'_'+QUANTITY+'_'+CUT+'_'+PDFs+('_'+args.outname if args.outname else '')+'.pdf')
            cZP.deleteCanvas()

            # Make PDF comparison plot for S+B/B
            cRat = Plotter.Canvas(lumi=pretty[MODEL]+'#rightarrow'+pretty[CHANNEL],ratioFactor=1./3,extra='Private Work Simulation')
            ratPlots = {PDF:{} for PDF in PDFstoCompare[PDFs]}
            for PDF in PDFstoCompare[PDFs]:
                zpFile = R.TFile('root/ZprimeInterferenceHists_'+MODEL+'_'+MASS+'_'+PDF+'_'+rootname[MODEL][PDF]+'.root')
                hname = MODEL+'To'+CHANNEL+('_M' if PDF=='NNPDF30nlo' else '_M')+MASS+'_Int'+hpdfname[PDF]
                zpHist = zpFile.Get(hname+'_'+QUANTITY+'_'+CUT).Clone() 
                zpHist.SetDirectory(0)
                zpHist.Rebin(REBIN)
                hist.GetXaxis().SetRangeUser(ranges[QUANTITY][0],ranges[QUANTITY][1])
                zpFile.Close()
                dyFile = R.TFile('root/ZprimeInterferenceHists_DY_'+PDF+'_'+rootname['DY'][PDF]+'.root')
                dyHist = dyFile.Get('DYTo'+CHANNEL+hpdfname[PDF]+'_'+QUANTITY+'_'+CUT).Clone()
                dyHist.SetDirectory(0)
                dyHist.Rebin(REBIN)
                hist.GetXaxis().SetRangeUser(ranges[QUANTITY][0],ranges[QUANTITY][1])
                dyFile.Close()
                
                #ratHist = zpHist.Clone(MODEL+'To'+CHANNEL+'_ResM'+MASS+'_DY_'+PDF+'_ratio')
                ratHist = zpHist.Clone(MODEL+'To'+CHANNEL+'_M'+MASS+'_DY_'+PDF+'_ratio')
                ratHist.Divide(dyHist)
                ratPlots[PDF] = Plotter.Plot(ratHist,legName=pretty[PDF],legType='l',option='hist')
                #ratGraph, r, erl, ery = tools.binomial_divide(zpHist.Clone(),dyHist.Clone(),confint=clopper_pearson_poisson_means,force_lt_1=False)
                #ratPlots[PDF] = Plotter.Plot(ratGraph,legName=pretty[PDF],legType='l',option='pe')
                cRat.addMainPlot(ratPlots[PDF])
                ratPlots[PDF].SetLineColor(colors[PDF])
                ratPlots[PDF].SetMarkerColor(colors[PDF])
                ratPlots[PDF].SetLineWidth(1)

            cRat.firstPlot.setTitles(X=axes[QUANTITY]['x'],Y='S+B / B')
            cRat.firstPlot.GetYaxis().SetRangeUser(0,2)
            cRat.makeLegend(pos='tl')
            cRat.legend.moveLegend(X=0.2)
            for PDF in PDFstoCompare[PDFs]:
                if PDF=='NNPDF30nlo':continue
                cRat.addRatioPlot(ratPlots[PDF],ratPlots['NNPDF30nlo'],color=colors[PDF],legName=PDF+' / NNPDF30nlo',ytit='Ratio',xtit=axes[QUANTITY]['x'],plusminus=1.)
            cRat.makeRatioLegend(pos='tl')
            cRat.finishCanvas()
            cRat.save('plots/Ratio_'+MODEL+'_M'+MASS+'_DY_'+CHANNEL+'_PDF_'+CUT+'_'+QUANTITY+'_'+PDFs+('_'+args.outname if args.outname else '')+'.pdf')
            cRat.deleteCanvas()

            # Make combined plot of S+B and B plus ratio
            cComb = Plotter.Canvas(lumi=pretty[MODEL]+'#rightarrow'+pretty[CHANNEL],ratioFactor=1./3,extra='Private Work Simulation')
            for PDF in PDFstoCompare[PDFs]:
                cComb.addMainPlot(zpPlots[PDF])
                cComb.addMainPlot(dyPlots[PDF],addToPlotList=False)
            for PDF in PDFstoCompare[PDFs]:
                zpPlots[PDF].SetLineWidth(1)
                zpPlots[PDF].SetLineColor(colors[PDF])
                dyPlots[PDF].SetLineWidth(1)
                dyPlots[PDF].SetLineColor(colors[PDF])
                dyPlots[PDF].SetLineStyle(R.kDashed)
            cComb.firstPlot.setTitles(X=axes[QUANTITY]['x'],Y=axes[QUANTITY]['y'])
            cComb.makeLegend(pos='tr')
            cComb.legend.moveLegend(X=-0.2)
            cComb.setMaximum(factor)
            cComb.mainPad.SetLogy(True)
            for PDF in PDFstoCompare[PDFs]:
                cComb.addRatioPlot(zpPlots[PDF],dyPlots[PDF],color=colors[PDF],ytit='S+B / B',xtit=axes[QUANTITY]['x'],plusminus=1.)
            cComb.cleanup('plots/'+MODEL+'To'+CHANNEL+'_M'+MASS+'_combined_'+QUANTITY+'_'+CUT+'_'+PDFs+('_'+args.outname if args.outname else '')+'.pdf')
