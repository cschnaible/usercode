'''
Purpose of script is to compare Drell-Yan spectra generated with 
POWHEG and PYTHIA and NNPDF3.0 (NLO)
Chris Schnaible
22 October 2018
'''
import ROOT as R
import argparse
import Plotter as Plotter
import glob 
R.gROOT.SetBatch(True)
parser = argparse.ArgumentParser(description='Options for plotting mass distributions')
parser.add_argument('-in','--inname',default='',type=str,help='Extra name to add to input ROOT file')
parser.add_argument('-out','--outname',default='',type=str,help='Extra name to add to output file')
args = parser.parse_args()

PDF = 'NNPDF30nlo'
colors = {
        'NNPDF30nlo':R.kGreen+1,
        }
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
        }
DATE = args.inname

massBinsLow  = ['120','200','400','800','1400','2300','3500','4500']#,'6000']
massBinsHigh = ['200','400','800','1400','2300','3500','4500','6000']#,'Inf']
powhegXS = { # in pb
        '2016':{
            # from AN-16-391
            '50'  :{'xs':1.975E3,'nevts':2967200},
            '120' :{'xs':1.932E1,'nevts':100000},
            '200' :{'xs':2.731,'nevts':100000},
            '400' :{'xs':2.41E-1,'nevts':98400},
            '800' :{'xs':1.678E-2,'nevts':100000},
            '1400':{'xs':1.39E-3,'nevts':95106},
            '2300':{'xs':8.948E-5,'nevts':100000},
            '3500':{'xs':4.135E-6,'nevts':100000},
            '4500':{'xs':4.56E-7,'nevts':100000},
            '6000':{'xs':2.06E-8,'nevts':100000},
            },
        '2017':{
            '50'  :{'xs':2112.905,'nevts':2961000},
            '120' :{'xs':20.553,'nevts':100000},
            '200' :{'xs':2.8862,'nevts':100000},
            '400' :{'xs':0.25126,'nevts':100000},
            '800' :{'xs':0.017075,'nevts':100000},
            '1400':{'xs':1.366E-3,'nevts':100000},
            '2300':{'xs':8.178E-5,'nevts':100000},
            '3500':{'xs':3.191E-6,'nevts':100000},
            '4500':{'xs':2.787E-7,'nevts':100000},
            '6000':{'xs':9.569E-9,'nevts':100000},
            },
        }
def make_powheg_dist(when):
    where = '/afs/cern.ch/user/a/alfloren/public/DY_ROOT/'+when
    ptCut = '(gen_lep_pt[0]>53 && gen_lep_pt[1]>53)'
    etaCut = '(abs(gen_lep_eta[0])<2.4 && abs(gen_lep_eta[1])<2.4)'
    hmin,hmax = 0,9000
    binwidth = 50
    nbins = (hmax-hmin)/binwidth
    hists = {low:{} for low in massBinsLow}
    for b,(low,high) in enumerate(zip(massBinsLow,massBinsHigh)):
        FIRST='+' if b>0 else ''
        inFile = R.TFile(where+'/ana_datamc_dy'+low+'to'+high+'.root')
        t = inFile.Get('SimpleNtupler/t')
        #NEVTS = t.GetEntries()
        hists[low] = R.TH1F('powhegHist_'+when+'_'+low,'',nbins,hmin,hmax)
        hists[low].Sumw2()
        #t.Draw('gen_dil_mass>>powhegHist_{when}_{low}'.format(when=when,low=low),'({ptCut} && {etaCut})*{LUMI}*{XS}/{NEVTS}'.format(ptCut=ptCut,etaCut=etaCut,LUMI=36300+42100,XS=powhegXS[when][low]['xs'],NEVTS=powhegXS[when][low]['nevts']),'goff')
        t.Draw('gen_res_mass>>powhegHist_{when}_{low}'.format(when=when,low=low),'({ptCut} && {etaCut})*{LUMI}*{XS}/{NEVTS}'.format(ptCut=ptCut,etaCut=etaCut,LUMI=36300+42100,XS=powhegXS[when][low]['xs'],NEVTS=powhegXS[when][low]['nevts']),'goff')
        hists[low].SetDirectory(0)
        inFile.Close()
    powhegHist = R.TH1F('powhegHist_'+when,'',nbins,hmin,hmax)
    for b,(low,high) in enumerate(zip(massBinsLow,massBinsHigh)):
        powhegHist.Add(hists[low])
    return powhegHist


# Make PDF comparison plot for DY
cDY = Plotter.Canvas(lumi=pretty['DY']+'#rightarrow ll',ratioFactor=1./3,extra='Private Work Simulation')
# PYTHIA file
inFile = R.TFile('root/ZprimeInterferenceHists_DY_'+PDF+'_'+DATE+'.root')
pythiaHist = inFile.Get('DYToLL'+hpdfname[PDF]).Clone()
pythiaHist.SetDirectory(0)
inFile.Close()
# POWHEG files
powhegHist = make_powheg_dist('2016')
#powheg17Hist = make_powheg_dist('2017')

pythiaPlot = Plotter.Plot(pythiaHist,legName='PYTHIA NNPDF3.0',legType='l',option='hist')
cDY.addMainPlot(pythiaPlot)
powhegPlot = Plotter.Plot(powhegHist,legName='POWHEG NNPDF3.0',legType='l',option='hist')
cDY.addMainPlot(powhegPlot)
#powheg17Plot = Plotter.Plot(powheg17Hist,legName='POWHEG NNPDF3.1',legType='l',option='hist')
#cDY.addMainPlot(powheg17Plot)

pythiaPlot.SetLineColor(R.kBlue)
pythiaPlot.SetLineWidth(1)
powhegPlot.SetLineColor(R.kOrange+1)
powhegPlot.SetLineWidth(1)
#powheg17Plot.SetLineColor(R.kGreen+1)
#powheg17Plot.SetLineWidth(1)

cDY.firstPlot.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
cDY.makeLegend(pos='tr')
cDY.legend.moveLegend(X=-0.2)
cDY.legend.resizeHeight()
cDY.setMaximum()
cDY.mainPad.SetLogy(True)
cDY.addRatioPlot(powhegPlot,pythiaPlot,legName='POWHEG (NNPDF3.0) / PYTHIA (NNPDF3.0)',color=R.kOrange+1,ytit='POWHEG / PYTHIA',xtit='mass [GeV]',option='le')
#cDY.addRatioPlot(powheg17Plot,pythiaPlot,legName='POWHEG (NNPDF3.1) / PYTHIA (NNPDF3.0)',ytit='Ratio',color=R.kGreen+1,xtit='mass [GeV]',option='le')
#cDY.makeRatioLegend(pos='tr')
#cDY.ratLegend.moveLegend(X=-0.2)
cDY.cleanup('plots/DYToLL_generator_comparison'+('_'+args.outname if args.outname else '')+'.pdf')

canvRatio = Plotter.Canvas(lumi='NNPDF3.0 (NLO) '+pretty['DY']+'#rightarrow ll',extra='Private Work Simulation')
ratioHist = powhegHist.Clone('ratioHist')
ratioHist.Divide(pythiaHist)
ratioPlot = Plotter.Plot(ratioHist,option='hist')
canvRatio.addMainPlot(ratioPlot)
canvRatio.firstPlot.GetYaxis().SetRangeUser(0,2)
canvRatio.firstPlot.setTitles(Y='POWHEG / PYTHIA',X='mass [GeV]')
canvRatio.cleanup('plots/DYToLL_generator_ratio'+('_'+args.outname if args.outname else '')+'.pdf')

#    linExp = R.TF1('linExp','[0]+[1]*x',6000,9000)
#    linExp.SetParameter(0,1.0)
#    linExp.SetParameter(1,3.33E-5)
#    histExp = R.TH1F('histExp','',nbins,hmin,hmax)
#    histExp.FillRandom(linExp.GetName(),100000)
#    powhegHist.Add(histExp)
