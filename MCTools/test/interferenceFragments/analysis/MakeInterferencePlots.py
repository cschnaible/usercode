import ROOT as R
import os
import Plotter
R.gROOT.SetBatch(True)
import argparse
parser = argparse.ArgumentParser(description='Options for plotting mass distributions')
parser.add_argument('-i','--inname',default='',type=str,help='Identifier string for input histograms')
parser.add_argument('-o','--outname',default='',type=str,help='Identifier string for output histograms')
parser.add_argument('-s','--scale',action='store_true',help='Add extra scaling to cross sections to make ratio Z\' / DY mostly continious')
parser.add_argument('-pdf','--pdf',action='store_true',help='Loop on list of PDFs')
args = parser.parse_args()

LUMI = 36300.

CHANNELS = ['EE','MuMu','LL']#,'GenMuMu']
ALLRESMASSES = [4000,4500,5000,5500,6000,6500,7000,7500,8000]
MASSBINS = ['120','200','400','800','1400','2300','3500','4500','6000','Inf']
#MODELS = ['ZPrimeQ','ZPrimeSSM','ZPrimePSI','ZPrimeN','ZPrimeSQ','ZPrimeI','ZPrimeEta','ZPrimeChi','ZPrimeR','ZPrimeB-L','ZPrimeLR','ZPrimeY','ZPrimeT3L']
ALLMODELS = ['ZPrimeQ','ZPrimeSSM','ZPrimeSQ','ZPrimeR','ZPrimeB-L','ZPrimeLR','ZPrimeY','ZPrimeT3L']
ALLPDFS = ['NNPDF30nlo','CT10nlo','CT14nlo','CT5L']

if args.pdf:
    PDFS = ['NNPDF30nlo']#,'CT10nlo','CT14nlo']
else:
    PDFS = ['']

MODELS = ['ZPrimeB-L','ZPrimeQ','ZPrimeSSM','ZPrimePSI','ZPrimeT3L']
RESMASSES = [4000,4500,5000,5500,6000,6500]

inFile = R.TFile.Open('root/ZprimeInterferenceHists'+('_'+args.inname if args.inname else '')+'.root')
inFile.ls()
outFile = R.TFile.Open('root/ZprimeInterferencePlots'+('_'+args.outname if args.outname else '')+'.root','recreate')

# no longer needed!
SCALE = {PDF:{MODEL:{RESMASS:{MASSBIN:{} for MASSBIN in MASSBINS[:-1]} for RESMASS in ALLRESMASSES} for MODEL in ALLMODELS} for PDF in ALLPDFS}
with open("crossSectionScalings.data") as f:
    for l,line in enumerate(f):
        if l==0: continue # first line is column labels
        if line.strip('\n')=='': continue # skip empty lines
        PDF,MODEL,RESMASS = line.split()[:3]
        for m,MASSBIN in enumerate(MASSBINS[:-1]):
            SCALE[PDF][MODEL][float(RESMASS)][MASSBIN] = eval(line.split()[3:][m])


dyhists = {}
zpinthists = {}
zphists = {}
for PDF in PDFS:
    for CHAN in CHANNELS:
        # Do DY histograms
        dyname = 'DYTo'+CHAN
        print dyname+'_M'+MASSBINS[0]+'To'+MASSBINS[1]+('_'+PDF if PDF else '')
        dyhists[dyname+('_'+PDF if PDF else '')] = inFile.Get(dyname+'_M'+MASSBINS[0]+'To'+MASSBINS[1]+('_'+PDF if PDF else '')).Clone(dyname+('_'+PDF if PDF else ''))
        for i in range(1,len(MASSBINS)-1):
            dyhist = inFile.Get(dyname+'_M'+MASSBINS[i]+'To'+MASSBINS[i+1]+('_'+PDF if PDF else '')).Clone()
            # any additional rescaling done here
            if MASSBINS[i]=='800' and PDF=='CT5L' and args.scale: dyhist.Scale(1.07/0.94)
            dyhists[dyname+('_'+PDF if PDF else '')].Add(dyhist)
        dyhists[dyname+('_'+PDF if PDF else '')].SetDirectory(0)
        outFile.cd()
        dyhists[dyname+('_'+PDF if PDF else '')].Write()
        # Do interference histograms
        for RES in RESMASSES:
            for MODEL in MODELS:
                zpname = MODEL+'To'+(CHAN if 'Gen' not in CHAN else 'LL')+'_M'+str(RES)
                zpintname = zpname+'_Int'
                for interference in [True]:#,False]:
                    if interference:
                        zpinthists[zpintname+('_'+PDF if PDF else '')] = inFile.Get(zpintname+'_M'+MASSBINS[0]+'To'+MASSBINS[1]+('_'+PDF if PDF else '')).Clone(zpintname+('_'+PDF if PDF else ''))
                        if args.scale:
                            zpinthists[zpintname+('_'+PDF if PDF else '')].Scale(SCALE[PDF][MODEL][RES][MASSBINS[0]])
                        for i in range(1,len(MASSBINS)-1):
                            zpinthist = inFile.Get(zpintname+'_M'+MASSBINS[i]+'To'+MASSBINS[i+1]+('_'+PDF if PDF else '')).Clone()
                            # any additional rescaling done here
                            #
                            if args.scale:
                                zpinthist.Scale(SCALE[PDF][MODEL][RES][MASSBINS[i]])
                            zpinthists[zpintname+('_'+PDF if PDF else '')].Add(zpinthist)
                        zpinthists[zpintname+('_'+PDF if PDF else '')].SetDirectory(0)
                        outFile.cd()
                        zpinthists[zpintname+('_'+PDF if PDF else '')].Write()
                    else:
                        zphists[zpname+('_'+PDF if PDF else '')] = inFile.Get(zpname+('_'+PDF if PDF else '')).Clone(zpname+('_'+PDF if PDF else ''))
                        zphists[zpname+('_'+PDF if PDF else '')].SetDirectory(0)
                        outFile.cd()
                        zphists[zpname+('_'+PDF if PDF else '')].Write()
                outFile.cd()
                # Draw stuff together here and make it pretty
                c = Plotter.Canvas(lumi='36.3 fb^{-1} (13 TeV)',ratioFactor=1./3,extra='Private Work Simulation')
                zPIntPlot = Plotter.Plot(zpinthists[zpintname+('_'+PDF if PDF else '')],legName='Drell-Yan x Z\'_{{{MODEL}}}'.format(MODEL=MODEL[6:]),legType='l',option='hist')
                dyPlot = Plotter.Plot(dyhists[dyname+('_'+PDF if PDF else '')],legName='Drell-Yan',legType='l',option='hist')
                #zPPlot = Plotter.Plot(zphists[zpname+('_'+PDF if PDF else '')],legName='Pure Z\'_{{{MODEL}}}'.format(MODEL=MODEL[6:]),legType='l',option='hist')
                c.addMainPlot(zPIntPlot)
                c.addMainPlot(dyPlot)
                #c.addMainPlot(zPPlot)
                c.firstPlot.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
                hmax = dyPlot.GetMaximum()*1.1
                c.firstPlot.GetYaxis().SetRangeUser(1e-6,hmax)
                c.makeLegend(pos='tr')
                c.legend.moveLegend(X=-0.2)
                c.setMaximum()
                dyPlot.SetLineColor(R.kBlack)
                zPIntPlot.SetLineColor(R.kRed)
                #zPPlot.SetLineColor(R.kOrange)
                c.mainPad.SetLogy(True)
                c.addRatioPlot(zPIntPlot,dyPlot,color=R.kRed,ytit='S+B / B',xtit='mass [GeV]',option='pe')
                c.finishCanvas()
                outFile.cd()
                c.Write(MODEL+'To'+(CHAN if 'Gen' not in CHAN else 'LL')+'_M'+str(RES)+'_all'+('_'+PDF if PDF else ''))
                c.save('plots/'+MODEL+'To'+(CHAN if 'Gen' not in CHAN else 'LL')+'_M'+str(RES)+('_'+PDF if PDF else '')+'_all'+('_'+args.outname if args.outname else '')+'.pdf')
                c.deleteCanvas()









# old but keep just in case

#
#SCALEold = {
#        'CT5L':{
#        'ZPrimeB-L':{
#            8000:{
#                '120':1.0/1.07,
#                '400':1.0/0.91,
#                },
#            7500:{
#                '120':0.99/1.1,
#                '2300':0.925/0.99,
#                },
#            7000:{
#                '2300':0.91/1.09,
#                },
#            6500:{
#                '120':1.0/1.1,
#                '800':0.98/0.92,
#                '1400':0.95/1.01,
#                '3500':0.9/0.74,
#                },
#            6000:{
#                '120':(1.0/1.14)*(0.725/0.8),
#                '200':(0.725/0.8),
#                '400':(0.725/0.8),
#                '800':(0.95/0.91)*(0.725/0.8),
#                '1400':(1.02/0.91)*(0.725/0.8),
#                '2300':(0.725/0.8),
#                '3500':(0.9/0.71)*(0.725/0.8),
#                },
#            4500:{
#                '120':0.96/1.06,
#                '200':0.96/1.06,
#                },
#            },
#        'ZPrimeQ':{
#            4000:{
#                '120':1.0/1.02,
#                '200':0.90/0.83,
#                },
#            6000:{
#                '400':0.98/0.91,
#                }
#            },
#        'ZPrimeSSM':{
#            6000:{
#                '120':1.0/1.06,
#                '200':0.98/1.07,
#                '400':1.0/0.88,
#                '800':0.96/1.02,
#                '2300':1.0/1.06,
#                },
#            },
#        'ZPrimeR':{
#            6000:{
#                '120':1.02/1.15,
#                '2300':0.87/0.92,
#                },
#            },
#        'ZPrimeLR':{
#            6000:{
#                '400':1.0/0.94,
#                '2300':1.0/1.09,
#                '800':1.0/0.93,
#                },
#            },
#        'ZPrimeY':{
#            6000:{
#                '400':1.02/0.86,
#                '2300':0.72/0.82,
#                },
#            },
#        'ZPrimeT3L':{
#            6000:{
#                '200':1.0/0.9,
#                '400':1.0/0.88,
#                '1400':0.92/0.95,
#                },
#            },
#        }
#        }
#
#for PDF in SCALEold.keys():
#    for MODEL in SCALEold[PDF].keys():
#        for RESMASS in SCALEold[PDF][MODEL].keys():
#            for MASSBIN in SCALEold[PDF][MODEL][RESMASS].keys():
#                print PDF,MODEL,RESMASS,MASSBIN
#                if SCALEold[PDF][MODEL][RESMASS][MASSBIN] == SCALE[PDF][MODEL][RESMASS][MASSBIN]:
#                    print 'True'
#                else:
#                    print 'False'
