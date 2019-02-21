'''
Takes in output ROOT file from MakeToyDistributions.py and plots
- Toy datasets from S+B and B hypotheses overlayed with respective pdfs
    - Includes likelihood-ratio value of that toy and corresponding p-value
- Scatter plots per-event S+B and B likelihood-ratio values vs mass
'''
import ROOT as R
import argparse
import Plotter as Plotter
import tools
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
CHANNELS = ['EE','MuMu']
BDIR = args.batchid
low = 0
high = 9000
binwidth = 50
nbins = (high-low)/binwidth
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

# ZPrimeT3LToEE_ResM6000_Int_NNPDF30nlo_NPE_5_NEVT_2520_M_600_9000_toys_batch_2016_2017_20181010.root
for CHAN in CHANNELS:
    BASE = MODEL+'To'+CHAN+'_ResM'+MASS+'_Int_'+PDF
    NEVT = 3678 if CHAN=='MuMu' else 2520

    # Get likelihood ratio distributions from 20k toy file
    lrFile = R.TFile('hists/'+BDIR+'/'+BASE+'_NPE_20000_NEVT_'+str(NEVT)+'_M_600_9000_'+BDIR+'.root')
    peTree = lrFile.Get('peData')
    lrxmin = min(peTree.GetMinimum('lambda_sb_pe'),peTree.GetMinimum('lambda_b_pe'))
    lrxmax = max(peTree.GetMaximum('lambda_sb_pe'),peTree.GetMaximum('lambda_b_pe'))
    lrbinlow = float(math.floor(lrxmin))
    lrbinhigh = float(math.ceil(lrxmax))
    lrbinwidth = 1.0
    lrnBins = (lrbinhigh-lrbinlow)/lrbinwidth

    sbPEHist = R.TH1F('sbPEHist','',int(lrnBins),lrbinlow,lrbinhigh)
    bPEHist = R.TH1F('bPEHist','',int(lrnBins),lrbinlow,lrbinhigh)
    peTree.Draw('lambda_sb_pe>>sbPEHist')
    peTree.Draw('lambda_b_pe>>bPEHist')
    sbPEHist.SetDirectory(0)
    bPEHist.SetDirectory(0)
    lrFile.Close()
    lrHists = {
        'sb':sbPEHist,
        'b':bPEHist,
    }

    # 
    toyFile = R.TFile('hists/'+BDIR+'/'+BASE+'_NPE_5_NEVT_'+str(NEVT)+'_M_600_9000_toys_'+BDIR+'.root')

    for t in range(5):

        toyTree = toyFile.Get('peData'+str(t))
        for model in ['sb','b']:
            modelName = 'S+B' if model=='sb' else 'B'



            hist = R.TH1F('toyData_'+CHAN+'_'+str(t),'',int(nbins),low,high)
            toyTree.Draw('mass_'+model+'>>{hname}'.format(hname=hist.GetName()))
            dataPlot = Plotter.Plot(hist,legName='Toy data',legType='pe',option='pe')
            sbHist = toyFile.Get(BASE).Clone()
            bHist = toyFile.Get('DYTo'+CHAN+'_'+PDF).Clone()
            if model=='sb':
                den = tools.get_integral(sbHist,600)[0]
            else:
                den = tools.get_integral(bHist,600)[0]
            norm = NEVT / den
            sbHist.Scale(norm)
            bHist.Scale(norm)

            sbPlot = Plotter.Plot(sbHist,legName=pretty[MODEL]+'#rightarrow'+pretty[CHAN],legType='l',option='hist')
            bPlot = Plotter.Plot(bHist,legName=pretty['DY']+'#rightarrow'+pretty[CHAN],legType='l',option='hist')
            toy_lr = toyTree.GetUserInfo().FindObject('lambda_'+model).GetVal()
            fSB,pSB,zSB = tools.get_f_and_pz_values(lrHists['sb'],toy_lr,'alt')
            fB,pB,zB = tools.get_f_and_pz_values(lrHists['b'],toy_lr,'null')

            sbtext = 'p_{{S+B}} = {pSB:6.3f}, Z_{{S+B}} = {zSB:5.3f}'.format(pSB=pSB,zSB=zSB)
            print sbtext
            btext = 'p_{{B}} = {pB:6.3f}, Z_{{B}} = {zB:5.3f}'.format(pB=pB,zB=zB)
            print btext
            ltext = '#lambda_{{data}} = {toy_lr:6.3f}'.format(toy_lr=toy_lr)
            print ltext
            for logy in [True,False]:
                # False = plot toy data linear high mass
                # True = plot toy data semilog full mass range
                ratioFactor = 1./3 if logy else 0
                canvToyData = Plotter.Canvas(ratioFactor=ratioFactor,logy=logy,lumi='Toy dataset #{t} from {modelName} hypothesis'.format(**locals()),extra='Private Work Simulation')
                # ZPrimeT3LToEE_ResM6000_Int_NNPDF30nlo
                # DYToEE_NNPDF30nlo
                canvToyData.addMainPlot(dataPlot)
                canvToyData.addMainPlot(sbPlot)
                canvToyData.addMainPlot(bPlot)

                sbPlot.SetLineColor(R.kOrange+1)
                bPlot.SetLineColor(R.kBlue)

                canvToyData.firstPlot.setTitles(X='mass [GeV]',Y='Events / {binwidth} GeV'.format(binwidth=binwidth))
                canvToyData.makeLegend(pos='tr')
                canvToyData.legend.moveLegend(X=-0.1)
                canvToyData.legend.resizeHeight()
                if not logy:
                    canvToyData.firstPlot.GetYaxis().SetRangeUser(0,100)
                    xup = float(MASS)
                    canvToyData.firstPlot.GetXaxis().SetRangeUser(1000,xup)
                else:
                    canvToyData.drawText(sbtext,pos=(0.5,0.7),align='tl')
                    canvToyData.drawText(btext,pos=(0.5,0.65),align='tl')
                    canvToyData.drawText(ltext,pos=(0.5,0.6),align='tl')
                    canvToyData.firstPlot.GetYaxis().SetRangeUser(1E-5,3E5)
                    canvToyData.addRatioPlot(dataPlot,sbPlot,color=R.kOrange+1,ytit='Toy data / MC',xtit='mass [GeV]',option='pe')
                    canvToyData.addRatioPlot(dataPlot,bPlot,color=R.kBlue,ytit='Toy data / MC',xtit='mass [GeV]',option='pe')
                linear = '' if logy else '_linear'
                canvToyData.cleanup('plots/'+BASE+'_'+model+linear+'_toy_'+str(t)+'_'+(args.outname if args.outname else '')+'.pdf',mode='BOB')


            # Plot full PE likelihood ratios
            tools.printStats(lrHists['sb'])
            tools.printStats(lrHists['b'])
            sbPEPlot = Plotter.Plot(lrHists['sb'],legName=MASS+' GeV',legType='l',option='hist')
            bPEPlot = Plotter.Plot(lrHists['b'],legName='Drell-Yan',legType='l',option='hist')

            canvPE = Plotter.Canvas(lumi=pretty[MODEL]+'#rightarrow'+pretty[CHAN],extra='Private Work Simulation')
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
            l = R.TLine(toy_lr,0,toy_lr,ymax)
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
            ltext = '#lambda_{{toy}} = {toy_lr:6.3f}'.format(toy_lr=toy_lr)
            print ltext
            canvPE.drawText(sbtext,pos=(0.2,0.7),align='tl')
            canvPE.drawText(btext,pos=(0.2,0.65),align='tl')
            canvPE.drawText(ltext,pos=(0.2,0.6),align='tl')
            canvPE.cleanup('plots/'+BASE+'_pe_nll_'+model+'_toy_'+str(t)+'_'+(args.outname if args.outname else '')+'.pdf',mode='BOB')
    toyFile.Close()
