import ROOT as R
import argparse
import Plotter as Plotter
import tools as t
import math
import glob
import numpy as np
import array
R.gROOT.SetBatch(True)

parser = argparse.ArgumentParser(description='Options for plotting mass distributions')
parser.add_argument('-out','--outname',default='',type=str,help='Extra name to add to output')
parser.add_argument('-bid','--batchid',default='batch_2016_2017_20181010',type=str,help='Input string and directory for input ROOT files')
parser.add_argument('-model','--model',default='ZPrimeB-L',type=str,help='Z\' sample, e.g. ZPrimeB-L, ZPrimePSI')
parser.add_argument('-pdf','--pdf',default='NNPDF30nlo',type=str,help='Loop on PDF sets')
args = parser.parse_args()

if args.model== 'all':
    MODELS = ['ZPrimeT3L','ZPrimeSSM','ZPrimePSI','ZPrimeQ']
    #MODELS = ['ZPrimeB-L','ZPrimeT3L','ZPrimeSSM','ZPrimePSI','ZPrimeQ',\
    #        'ZPrimeR','ZPrimeLR','ZPrimeY']
else:
    MODELS = [args.model]
PDF = args.pdf
DIR = 'hists/'+args.batchid+'/'
CHANNELS = ['EE','MuMu']
MASSES = ['4000','4500','5000','5500','6000','6500','7000','7500','8000']

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
        return 'Z\'_{'+name[6:]+'}'
    else:
        return pretty[name]

masses = array.array('d',[4000,4500,5000,5500,6000,6500,7000,7500,8000])
# hists/batch_2016_2017_20181010/
# ZPrimePSIToMuMu_ResM6000_Int_NNPDF30nlo_NPE_20000_NEVT_3678_M_600_9000_batch_2016_2017_20181010.root
plotTypes = ['eventMean','eventRMS','PEMean','PERMS','pValue','zValue']
allPlots = {plot:{CHAN:{MODEL:{'SB':{},'B':{}} for MODEL in MODELS} for CHAN in CHANNELS} for plot in plotTypes}
# ZPrimeB-LToEE_ResM7500_Int_NNPDF30nlo_hist_nll_event_sb
# ZPrimeB-LToEE_ResM7500_Int_NNPDF30nlo_hist_nll_event_b
# Plot per event likelihood ratios vs. mass
for CHANNEL in CHANNELS:
    NEVT = '3678' if CHANNEL=='MuMu' else '2520'
    for MODEL in MODELS:
        perEvtMean_SB = []
        perEvtMean_B = []
        perEvtRMS_SB = []
        perEvtRMS_B = []
        for MASS in MASSES:
            BASE = MODEL+'To'+CHANNEL+'_ResM'+MASS+'_Int_'+PDF
            inFile = R.TFile(DIR+BASE+'_NPE_20000_NEVT_'+NEVT+'_M_600_9000_'+args.batchid+'.root')

            sbEvtHist = inFile.Get(BASE+'_hist_nll_event_sb').Clone()
            t.printStats(sbEvtHist)
            mean_sb = sbEvtHist.GetMean()
            rms_sb = sbEvtHist.GetRMS()
            perEvtMean_SB.append(mean_sb)
            perEvtRMS_SB.append(rms_sb)

            bEvtHist = inFile.Get(BASE+'_hist_nll_event_b').Clone()
            t.printStats(bEvtHist)
            mean_b = bEvtHist.GetMean()
            rms_b = bEvtHist.GetRMS()
            perEvtMean_B.append(mean_b)
            perEvtRMS_B.append(rms_b)
            inFile.Close()

        # Per-event likelihood ratio mean
        canvEvtMean = Plotter.Canvas(lumi=get_pretty(MODEL)+'#rightarrow'+get_pretty(CHANNEL),extra='Private Work Simulation')
        graph_mean_SB = R.TGraph(len(masses),masses,array.array('d',perEvtMean_SB))
        print masses
        print perEvtMean_SB
        graph_mean_B = R.TGraph(len(masses),masses,array.array('d',perEvtMean_B))
        plot_mean_SB = Plotter.Plot(graph_mean_SB,legName=get_pretty(MODEL),legType='lp',option='lp')
        plot_mean_B = Plotter.Plot(graph_mean_B,legName=get_pretty('DY'),legType='lp',option='lp')
        canvEvtMean.addMainPlot(plot_mean_SB)
        canvEvtMean.addMainPlot(plot_mean_B)
        plot_mean_SB.SetLineColor(R.kOrange+1)
        plot_mean_B.SetLineColor(R.kBlue)
        plot_mean_SB.SetMarkerColor(R.kOrange+1)
        plot_mean_B.SetMarkerColor(R.kBlue)
        ymin_mean = min(min(perEvtMean_SB), min(perEvtMean_B))
        ymax_mean = max(max(perEvtMean_SB), max(perEvtMean_B))
        canvEvtMean.firstPlot.GetHistogram().SetMinimum(1.1*ymin_mean)
        canvEvtMean.firstPlot.GetHistogram().SetMaximum(1.1*ymax_mean)
        #canvEvtMean.firstPlot.GetYaxis().SetRangeUser(1.1*ymin_mean,1.1*ymax_mean)
        canvEvtMean.firstPlot.setTitles(X='mass [GeV]',Y='Per-event mean #lambda')
        canvEvtMean.makeLegend(pos='tr')
        canvEvtMean.legend.resizeHeight()
        canvEvtMean.cleanup('plots/'+MODEL+'_'+CHANNEL+'_'+PDF+'_perEvt_LR_mean_vs_mass'+('_'+args.outname if args.outname else '')+'.pdf')

        # Per-event likelihood ratio rms
        canvEvtRMS = Plotter.Canvas(lumi=get_pretty(MODEL)+'#rightarrow'+get_pretty(CHANNEL),extra='Private Work Simulation')
        graph_rms_SB = R.TGraph(len(masses),masses,array.array('d',perEvtRMS_SB))
        graph_rms_B = R.TGraph(len(masses),masses,array.array('d',perEvtRMS_B))
        plot_rms_SB = Plotter.Plot(graph_rms_SB,legName=get_pretty(MODEL),legType='lp',option='lp')
        plot_rms_B = Plotter.Plot(graph_rms_B,legName=get_pretty('DY'),legType='lp',option='lp')
        canvEvtRMS.addMainPlot(plot_rms_SB)
        canvEvtRMS.addMainPlot(plot_rms_B)
        plot_rms_SB.SetLineColor(R.kOrange+1)
        plot_rms_B.SetLineColor(R.kBlue)
        plot_rms_SB.SetMarkerColor(R.kOrange+1)
        plot_rms_B.SetMarkerColor(R.kBlue)
        ymin_rms = 0.#min(min(perEvtRMS_SB), min(perEvtRMS_B))
        ymax_rms = max(max(perEvtRMS_SB), max(perEvtRMS_B))
        canvEvtRMS.firstPlot.GetHistogram().SetMinimum(1.1*ymin_rms)
        canvEvtRMS.firstPlot.GetHistogram().SetMaximum(1.1*ymax_rms)
        #canvEvtRMS.firstPlot.GetYaxis().SetRangeUser(0.9*ymin_rms,1.1*ymax_rms)
        canvEvtRMS.firstPlot.setTitles(X='mass [GeV]',Y='Per-event rms #lambda')
        canvEvtRMS.makeLegend(pos='tr')
        canvEvtRMS.legend.resizeHeight()
        canvEvtRMS.cleanup('plots/'+MODEL+'_'+CHANNEL+'_'+PDF+'_perEvt_LR_rms_vs_mass'+('_'+args.outname if args.outname else '')+'.pdf')



# Plot likelihood ratio mean and rms for all PE vs mass
# Plot p/z-values for all PE vs mass
for CHANNEL in CHANNELS:
    NEVT = '3678' if CHANNEL=='MuMu' else '2520'
    for MODEL in MODELS:
        perPEMean_sb = []
        perPEMean_b = []
        perPERMS_sb = []
        perPERMS_b = []
        pValue_sb = []
        pValue_b = []
        zValue_sb = []
        zValue_b = []
        data_lr = []
        for MASS in MASSES:
            BASE = MODEL+'To'+CHANNEL+'_ResM'+MASS+'_Int_'+PDF
            inFile = R.TFile(DIR+BASE+'_NPE_20000_NEVT_'+NEVT+'_M_600_9000_'+args.batchid+'.root')
            print inFile

            peTree = inFile.Get('peData')
            print peTree
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
            perPEMean_sb.append(sbPEHist.GetMean())
            perPERMS_sb.append(sbPEHist.GetRMS())
            t.printStats(bPEHist)
            perPEMean_b.append(bPEHist.GetMean())
            perPERMS_b.append(bPEHist.GetRMS())

            dataVal = peTree.GetUserInfo().FindObject('lambda_d').GetVal()
            data_lr.append(dataVal)
            fSB,pSB,zSB = t.get_f_and_pz_values(sbPEHist,dataVal,'alt')
            fB,pB,zB    = t.get_f_and_pz_values(bPEHist,dataVal,'null')

            pValue_sb.append(pSB)
            pValue_b.append(pB)
            zValue_sb.append(zSB)
            zValue_b.append(zB)

            inFile.Close()
        # Pseudoexperiment likelihood ratio mean vs. mass
        canvPEMean = Plotter.Canvas(lumi=get_pretty(MODEL)+'#rightarrow'+get_pretty(CHANNEL),extra='Private Work')
        graph_pe_mean_sb = R.TGraph(len(masses),masses,array.array('d',perPEMean_sb))
        graph_pe_mean_b = R.TGraph(len(masses),masses,array.array('d',perPEMean_b))
        plot_pe_mean_sb = Plotter.Plot(graph_pe_mean_sb,legName=get_pretty(MODEL),legType='pe',option='lp')
        plot_pe_mean_b = Plotter.Plot(graph_pe_mean_b,legName=get_pretty('DY'),legType='pe',option='lp')
        canvPEMean.addMainPlot(plot_pe_mean_sb)
        canvPEMean.addMainPlot(plot_pe_mean_b)
        plot_pe_mean_sb.SetLineColor(R.kOrange+1)
        plot_pe_mean_b.SetLineColor(R.kBlue)
        plot_pe_mean_sb.SetMarkerColor(R.kOrange+1)
        plot_pe_mean_b.SetMarkerColor(R.kBlue)
        ymin_mean = min(min(perPEMean_sb), min(perPEMean_b))
        ymax_mean = max(max(perPEMean_sb), max(perPEMean_b))
        canvPEMean.firstPlot.GetHistogram().SetMaximum(1.1*ymax_mean)
        canvPEMean.firstPlot.GetHistogram().SetMinimum(1.1*ymin_mean)
        #canvPEMean.firstPlot.GetYaxis().SetRangeUser(1.1*ymin_mean,1.1*ymax_mean)
        canvPEMean.firstPlot.setTitles(X='mass [GeV]',Y='Pseudoexperiment #lambda mean')
        canvPEMean.makeLegend(pos='tr')
        canvPEMean.legend.resizeHeight()
        canvPEMean.cleanup('plots/'+MODEL+'_'+CHANNEL+'_'+PDF+'_PE_LR_mean_vs_mass'+('_'+args.outname if args.outname else '')+'.pdf')

        # Pseudoexperiment likelihood ratio rms vs. mass
        canvPERMS = Plotter.Canvas(lumi=get_pretty(MODEL)+'#rightarrow'+get_pretty(CHANNEL),extra='Private Work')
        graph_pe_rms_sb = R.TGraph(len(masses),masses,array.array('d',perPERMS_sb))
        graph_pe_rms_b = R.TGraph(len(masses),masses,array.array('d',perPERMS_b))
        plot_pe_rms_sb = Plotter.Plot(graph_pe_rms_sb,legName=get_pretty(MODEL),legType='pe',option='lp')
        plot_pe_rms_b = Plotter.Plot(graph_pe_rms_b,legName=get_pretty('DY'),legType='pe',option='lp')
        canvPERMS.addMainPlot(plot_pe_rms_sb)
        canvPERMS.addMainPlot(plot_pe_rms_b)
        plot_pe_rms_sb.SetLineColor(R.kOrange+1)
        plot_pe_rms_b.SetLineColor(R.kBlue)
        plot_pe_rms_sb.SetMarkerColor(R.kOrange+1)
        plot_pe_rms_b.SetMarkerColor(R.kBlue)
        ymin_rms = 0.#min(min(perPERMS_sb), min(perPERMS_b))
        ymax_rms = max(max(perPERMS_sb), max(perPERMS_b))
        canvPERMS.firstPlot.GetHistogram().SetMinimum(ymin_rms)
        canvPERMS.firstPlot.GetHistogram().SetMaximum(1.1*ymax_rms)
        #canvPERMS.firstPlot.GetYaxis().SetRangeUser(ymin_rms,1.1*ymax_rms)
        canvPERMS.firstPlot.setTitles(X='mass [GeV]',Y='Pseudoexperiment #lambda RMS')
        canvPERMS.makeLegend(pos='tr')
        canvPERMS.legend.resizeHeight()
        canvPERMS.cleanup('plots/'+MODEL+'_'+CHANNEL+'_'+PDF+'_PE_LR_rms_vs_mass'+('_'+args.outname if args.outname else '')+'.pdf')

        # Data SB and B p-value vs mass 
        canvPvalue = Plotter.Canvas(lumi=get_pretty(MODEL)+'#rightarrow'+get_pretty(CHANNEL),logy=True,extra='Private Work')
        graph_p_sb = R.TGraph(len(masses),masses,array.array('d',pValue_sb))
        graph_p_b = R.TGraph(len(masses),masses,array.array('d',pValue_b))
        plot_p_sb = Plotter.Plot(graph_p_sb,legName=get_pretty(MODEL),legType='pe',option='lp')
        plot_p_b = Plotter.Plot(graph_p_b,legName=get_pretty('DY'),legType='pe',option='lp')
        canvPvalue.addMainPlot(plot_p_sb)
        canvPvalue.addMainPlot(plot_p_b)
        plot_p_sb.SetLineColor(R.kOrange+1)
        plot_p_b.SetLineColor(R.kBlue)
        plot_p_sb.SetMarkerColor(R.kOrange+1)
        plot_p_b.SetMarkerColor(R.kBlue)
        ymin_p = min(min(pValue_sb), min(pValue_b))*0.1
        ymax_p = 1.1#max(max(pValue_sb), max(pValue_b))
        canvPvalue.firstPlot.GetHistogram().SetMinimum(ymin_p)
        canvPvalue.firstPlot.GetHistogram().SetMaximum(ymax_p)
        #canvPvalue.firstPlot.GetYaxis().SetRangeUser(ymin_p,ymax_p)
        canvPvalue.firstPlot.setTitles(X='mass [GeV]',Y='p-value')
        canvPvalue.makeLegend(pos='tr')
        canvPvalue.legend.resizeHeight()
        canvPvalue.cleanup('plots/'+MODEL+'_'+CHANNEL+'_'+PDF+'_p_value_vs_mass'+('_'+args.outname if args.outname else '')+'.pdf')

        # Data SB and B z-value vs mass 
        canvZvalue = Plotter.Canvas(lumi=get_pretty(MODEL)+'#rightarrow'+get_pretty(CHANNEL),extra='Private Work')
        graph_z_sb = R.TGraph(len(masses),masses,array.array('d',zValue_sb))
        graph_z_b = R.TGraph(len(masses),masses,array.array('d',zValue_b))
        plot_z_sb = Plotter.Plot(graph_z_sb,legName=get_pretty(MODEL),legType='pe',option='lp')
        plot_z_b = Plotter.Plot(graph_z_b,legName=get_pretty('DY'),legType='pe',option='lp')
        allPlots['zValue'][CHANNEL][MODEL]['SB'] = plot_z_sb
        allPlots['zValue'][CHANNEL][MODEL]['B'] = plot_z_b
        canvZvalue.addMainPlot(plot_z_sb)
        canvZvalue.addMainPlot(plot_z_b)
        plot_z_sb.SetLineColor(R.kOrange+1)
        plot_z_b.SetLineColor(R.kBlue)
        plot_z_sb.SetMarkerColor(R.kOrange+1)
        plot_z_b.SetMarkerColor(R.kBlue)
        ymin_rms = min(min(zValue_sb), min(zValue_b))
        ymax_rms = max(max(zValue_sb), max(zValue_b))
        canvZvalue.firstPlot.GetHistogram().SetMinimum(1.1*ymin_rms)
        canvZvalue.firstPlot.GetHistogram().SetMaximum(1.1*ymax_rms)
        #canvZvalue.firstPlot.GetYaxis().SetRangeUser(1.1*ymin_rms,1.1*ymax_rms)
        canvZvalue.firstPlot.setTitles(X='mass [GeV]',Y='Z-value')
        canvZvalue.makeLegend(pos='tr')
        canvZvalue.legend.resizeHeight()
        canvZvalue.cleanup('plots/'+MODEL+'_'+CHANNEL+'_'+PDF+'_z_value_vs_mass'+('_'+args.outname if args.outname else '')+'.pdf')

colors = {
        'ZPrimeQ':R.kCyan+4,
        'ZPrimeSSM':R.kOrange+1,
        'ZPrimeT3L':R.kRed,

        'ZPrimeB-L':R.kBlue,
        'ZPrimeLR':R.kGreen+1,
        'ZPrimeR':R.kMagenta+1,
        'ZPrimeY':R.kRed+3,

        'ZPrimePSI':R.kViolet+5,
        'ZPrimeChi':R.kYellow-3,
        'ZPrimeEta':R.kCyan+2,
        'ZPrimeN':R.kGray,
        'ZPrimeI':R.kAzure+5,
        'ZPrimeSQ':R.kCyan,
        }
if args.model=='all':
    # plot multiple models together
    for CHANNEL in CHANNELS:
        # plot z-value vs mass
        canvZvalue = Plotter.Canvas(lumi='',extra='Private Work')
        for MODEL in MODELS:
            canvZvalue.addMainPlot(allPlots['zValue'][CHANNEL][MODEL]['SB'])
            canvZvalue.addMainPlot(allPlots['zValue'][CHANNEL][MODEL]['B'],addToPlotList=False)
        for MODEL in MODELS:
            allPlots['zValue'][CHANNEL][MODEL]['SB'].SetLineColor(colors[MODEL])
            allPlots['zValue'][CHANNEL][MODEL]['B'].SetLineColor(colors[MODEL])
            allPlots['zValue'][CHANNEL][MODEL]['B'].SetLineStyle(R.kDashed)
            allPlots['zValue'][CHANNEL][MODEL]['SB'].SetMarkerColor(colors[MODEL])
            allPlots['zValue'][CHANNEL][MODEL]['B'].SetMarkerColor(colors[MODEL])
        lim = 7
        canvZvalue.firstPlot.GetHistogram().SetMinimum(-lim)
        canvZvalue.firstPlot.GetHistogram().SetMaximum(lim)
        canvZvalue.firstPlot.setTitles(X='mass [GeV]',Y='Z-value')
        canvZvalue.makeLegend(pos='tr')
        canvZvalue.legend.resizeHeight()
        canvZvalue.cleanup('plots/allModels_'+CHANNEL+'_'+PDF+'_z_value_vs_mass'+('_'+args.outname if args.outname else '')+'.pdf')
        for plot in ['SB','B']:
            # plot z-value vs mass
            canvZvalue = Plotter.Canvas(lumi='',extra='Private Work')
            for MODEL in MODELS:
                canvZvalue.addMainPlot(allPlots['zValue'][CHANNEL][MODEL][plot])
            for MODEL in MODELS:
                allPlots['zValue'][CHANNEL][MODEL][plot].SetLineColor(colors[MODEL])
                if plot=='B': allPlots['zValue'][CHANNEL][MODEL]['B'].SetLineStyle(R.kDashed)
                allPlots['zValue'][CHANNEL][MODEL][plot].SetMarkerColor(colors[MODEL])
            lim = 7
            canvZvalue.firstPlot.GetHistogram().SetMinimum(-lim)
            canvZvalue.firstPlot.GetHistogram().SetMaximum(lim)
            canvZvalue.firstPlot.setTitles(X='mass [GeV]',Y='Z-value')
            canvZvalue.makeLegend(pos='tr')
            canvZvalue.legend.resizeHeight()
            canvZvalue.cleanup('plots/allModels_'+CHANNEL+'_'+PDF+'_'+plot+'_z_value_vs_mass'+('_'+args.outname if args.outname else '')+'.pdf')
