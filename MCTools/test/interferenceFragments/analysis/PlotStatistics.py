'''
Purpose of this script is to plot test statistics for a single Z' model
Comparison of S+B and B pdfs:
- per-event likelihood ratio
- full PE likelihood ratio
- full PE likelihood ratio (with data)
Options:
- model
- PDF
'''
import ROOT as R
import argparse
import Plotter as Plotter
import tools as t
import math
import glob
R.gROOT.SetBatch(True)

parser = argparse.ArgumentParser(description='Options for plotting mass distributions')
parser.add_argument('-out','--outname',default='',type=str,help='Extra name to add to output')
parser.add_argument('-bid','--batchid',default='batch_2016_2017_20181010',type=str,help='Input string and directory for input ROOT files')
parser.add_argument('-model','--model',default='ZPrimeB-L',type=str,help='Z\' sample, e.g. ZPrimeB-L, ZPrimePSI')
parser.add_argument('-mass','--mass',default='6000',type=str,help='Resonance mass for Z\' sample')
parser.add_argument('-pdf','--pdf',default='NNPDF30nlo',type=str,help='Loop on PDF sets')
args = parser.parse_args()

MODEL = args.model
MASS = args.mass
PDF = args.pdf
DIR = 'hists/'+args.batchid+'/'

CHANNELS = ['MuMu','EE']
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
pretty = {
        'MuMu':'#mu#mu',
        'EE':'ee',
        'LL':'ll',
        'ZPrime'+MODEL[6:]:'Z\'_{'+MODEL.strip('ZPrime')+'}',
        'DY':'Z^{0}/#gamma',
        'NNPDF30nlo':'NNPDF 3.0 (NLO)',
        'CT10nlo':'CT10 (NLO)',
        'CT14nlo':'CT14 (NLO)',
        'CTEQ5L':'CTEQ 5L (LO)',
        }
# hists/batch_2016_2017_20181010/
# ZPrimePSIToMuMu_ResM6000_Int_NNPDF30nlo_NPE_20000_NEVT_3678_M_600_9000_batch_2016_2017_20181010.root
for CHANNEL in CHANNELS:
    NEVT = '3678' if CHANNEL=='MuMu' else '2520'
    BASE = MODEL+'To'+CHANNEL+'_ResM'+MASS+'_Int_'+PDF
    inFile = R.TFile(DIR+BASE+'_NPE_20000_NEVT_'+NEVT+'_M_600_9000_'+args.batchid+'.root')

    # Plot per event likelihood ratios
    # ZPrimeB-LToEE_ResM7500_Int_NNPDF30nlo_hist_nll_event_sb
    # ZPrimeB-LToEE_ResM7500_Int_NNPDF30nlo_hist_nll_event_b
    canvEvt = Plotter.Canvas(lumi=pretty[MODEL]+'#rightarrow'+pretty[CHANNEL],logy=True,extra='Private Work Simulation')
    sbEvtHist = inFile.Get(BASE+'_hist_nll_event_sb').Clone()
    t.printStats(sbEvtHist)
    sbEvtHist.Rebin(2)
    sbEvtPlot = Plotter.Plot(sbEvtHist,legName=MASS+' GeV',legType='l',option='hist')
    bEvtHist = inFile.Get(BASE+'_hist_nll_event_b').Clone()
    t.printStats(bEvtHist)
    bEvtHist.Rebin(2)
    bEvtPlot = Plotter.Plot(bEvtHist,legName='Drell-Yan',legType='l',option='hist')
    canvEvt.addMainPlot(sbEvtPlot)
    canvEvt.addMainPlot(bEvtPlot)
    sbEvtPlot.SetLineColor(colors[MASS])
    sbEvtPlot.SetLineWidth(1)
    bEvtPlot.SetLineWidth(1)
    canvEvt.firstPlot.setTitles(X='-2 ln#(){L_{S+B} / L_{B}}',Y='Events')
    canvEvt.firstPlot.GetXaxis().SetRangeUser(-15,5)
    canvEvt.setMaximum()
    canvEvt.makeLegend(pos='tl')
    canvEvt.legend.resizeHeight()
    canvEvt.cleanup('plots/'+BASE+'_event_nll'+('_'+args.outname if args.outname else '')+'.pdf')

    # Plot full PE likelihood ratios
    peTree = inFile.Get('peData')
    xmin = min(peTree.GetMinimum('lambda_sb_pe'),peTree.GetMinimum('lambda_b_pe'))
    xmax = max(peTree.GetMaximum('lambda_sb_pe'),peTree.GetMaximum('lambda_b_pe'))
    binlow = float(math.floor(xmin))
    binhigh = float(math.ceil(xmax))
    binwidth = 1.0
    nBins = (binhigh-binlow)/binwidth

    sbPEHist = R.TH1F('sbPEHist','',int(nBins),binlow,binhigh)
    bPEHist = R.TH1F('bPEHist','',int(nBins),binlow,binhigh)
    peTree.Draw('lambda_sb_pe>>sbPEHist')
    peTree.Draw('lambda_b_pe>>bPEHist')
    t.printStats(sbPEHist)
    t.printStats(bPEHist)
    sbPEPlot = Plotter.Plot(sbPEHist,legName=MASS+' GeV',legType='l',option='hist')
    bPEPlot = Plotter.Plot(bPEHist,legName='Drell-Yan',legType='l',option='hist')

    for data in [True,False]:
        canvPE = Plotter.Canvas(lumi=pretty[MODEL]+'#rightarrow'+pretty[CHANNEL],extra='Private Work Simulation')
        canvPE.addMainPlot(sbPEPlot)
        canvPE.addMainPlot(bPEPlot)
        sbPEPlot.SetLineColor(colors[MASS])
        sbPEPlot.SetLineWidth(1)
        bPEPlot.SetLineWidth(1)
        canvPE.firstPlot.setTitles(X='-2 ln#(){L_{S+B} / L_{B}}',Y='Pseudo-experiments')
        canvPE.makeLegend(pos='tl')
        canvPE.legend.resizeHeight()
        canvPE.setMaximum()
        ymax = max(sbPEPlot.GetMaximum(),bPEPlot.GetMaximum())
        if data:
            data_lr = peTree.GetUserInfo().FindObject('lambda_d').GetVal()
            fSB,pSB,zSB = t.get_f_and_pz_values(sbPEHist,data_lr,'alt')
            fB,pB,zB    = t.get_f_and_pz_values(bPEHist,data_lr,'null')
            l = R.TLine(data_lr,0,data_lr,ymax)
            l.Draw()
            l.SetLineWidth(2)
            fSB.SetLineWidth(1)
            fSB.SetLineStyle(R.kDashed)
            fSB.SetLineColor(colors[MASS])
            fB.SetLineWidth(1)
            fB.SetLineStyle(R.kDashed)
            fSB.Draw('same')
            fB.Draw('same')
            sbtext = 'p_{{S+B}} = {pSB:6.3f}, Z_{{S+B}} = {zSB:5.3f}'.format(pSB=pSB,zSB=zSB)
            print sbtext
            btext = 'p_{{B}} = {pB:6.3f}, Z_{{B}} = {zB:5.3f}'.format(pB=pB,zB=zB)
            print btext
            ltext = '#lambda_{{data}} = {data_lr:6.3f}'.format(data_lr=data_lr)
            print ltext
            canvPE.drawText(sbtext,pos=(0.2,0.7),align='tl')
            canvPE.drawText(btext,pos=(0.2,0.65),align='tl')
            canvPE.drawText(ltext,pos=(0.2,0.6),align='tl')
        canvPE.cleanup('plots/'+BASE+'_pe_nll'+('_data' if data else '')+('_'+args.outname if args.outname else '')+'.pdf')



## Plot likelihood ratio for all PE (histograms)
#for data in [False]:#,True]:
#    canvPE = Plotter.Canvas(lumi=pretty[MODEL]+'#rightarrow'+pretty[CHANNEL],extra='Private Work Simulation')
#    sbPEHist = inFile.Get(BASE+'_hist_nll_pe_sb').Clone()
#    t.printStats(sbPEHist)
#    sbPEHist.Rebin(5)
#    sbPEPlot = Plotter.Plot(sbPEHist,legName=MASS+' GeV',legType='l',option='hist')
#    bPEHist = inFile.Get(BASE+'_hist_nll_pe_b').Clone()
#    t.printStats(bPEHist)
#    bPEHist.Rebin(5)
#    bPEPlot = Plotter.Plot(bPEHist,legName='Drell-Yan',legType='l',option='hist')
#    canvPE.addMainPlot(sbPEPlot)
#    canvPE.addMainPlot(bPEPlot)
#    sbPEPlot.SetLineColor(colors[MASS])
#    sbPEPlot.SetLineWidth(1)
#    bPEPlot.SetLineWidth(1)
#    canvPE.firstPlot.setTitles(X='-2 ln#(){L_{S+B} / L_{B}}',Y='Events')
#    canvPE.firstPlot.GetXaxis().SetRangeUser(-200,75)
#    canvPE.setMaximum()
#    canvPE.makeLegend(pos='tl')
#    canvPE.legend.resizeHeight()
#    canvPE.cleanup('plots/'+BASE+'_event_nll'+('_'+args.name if args.name else '')+'.pdf')

# Plot likelihood ratio for all PE (tree)
