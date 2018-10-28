import ROOT as R
import argparse
import Plotter as Plotter
import tools as t
R.gROOT.SetBatch(True)

parser = argparse.ArgumentParser(description='Options for plotting mass distributions')
parser.add_argument('-n','--name',default='',type=str,help='Identifier for input ROOT file')
parser.add_argument('-o','--out',default='',type=str,help='Extra name to add to output')
parser.add_argument('-zp','--zprime',default='B-L',help='Which models to plot')
parser.add_argument('-c','--channel',default='MuMu',help='Which models to plot')
parser.add_argument('-m','--mass',default=4000,help='Which resonance mass to plot')
parser.add_argument('-dy','--drellyan',action='store_true',help='Draw drell-yan (kills -m and -zp options if specified)')
#parser.add_argument('-m','--mass',default='6000',help='Which mass to plot')
args = parser.parse_args()

massbins = ['120','200','400','800','1400','2300','3500','4500','6000','Inf']
colors = {# defined by low edge of mass bin
        120:R.kRed-7,
        200:R.kRed+2,
        400:R.kMagenta-7,
        800:R.kMagenta+2,
        1400:R.kBlue-7,
        2300:R.kBlue+2,
        3500:R.kGreen-3,
        4500:R.kGreen+3,
        6000:R.kOrange+1,
        }

inFile = R.TFile('ZprimeInterference'+('_'+args.name if args.name else '')+'.root')

if args.drellyan:
    lumi = 'DY#rightarrow#mu#mu'
    hnamebase = 'DYTo'+args.channel
else:
    lumi = 'Z\'_{'+args.zprime+'}#rightarrow#mu#mu'
    hnamebase = 'ZPrime'+args.zprime+'To'+args.channel+'_M'+str(args.mass)+'_Int'

# Plot mass bins together
c = Plotter.Canvas(lumi=lumi,logy=True,extra='Private Work Simulation')
plots = {massbins[i]:{} for i in range(len(massbins)-1)}
for i in range(len(massbins)-1):
    hname = hnamebase+'_M'+massbins[i]+'To'+massbins[i+1]
    print hname
    plots[massbins[i]] = Plotter.Plot(inFile.Get(hname).Clone(),legName=massbins[i]+' to '+massbins[i+1],legType='l',option='hist')
    c.addMainPlot(plots[massbins[i]])
    plots[massbins[i]].SetLineColor(colors[int(massbins[i])])
    plots[massbins[i]].SetLineWidth(1)
c.firstPlot.setTitles(X='mass [GeV]',Y='Events / 50 GeV')
c.firstPlot.GetYaxis().SetRangeUser(1e-7,1e7)
c.makeLegend(pos='tr')
c.legend.resizeHeight()
c.legend.moveLegend(X=-0.2)
c.cleanup('plots/'+hnamebase+'_MassBinsSeparate.pdf')

# Plot mass bins stacked
c = Plotter.Canvas(lumi=lumi,logy=True,extra='Private Work Simulation')
c.makeLegend(pos='tr')
s = R.THStack(hnamebase+'_stack','')
splot = Plotter.Stack(s,option='hist')
plots_stack = {massbins[i]:{} for i in range(len(massbins)-1)}
massbinsrev = massbins[::-1]
for m in range(len(massbinsrev)-1):
    hname = hnamebase+'_M'+massbinsrev[m+1]+'To'+massbinsrev[m]
    print hname
    plots_stack[massbinsrev[m+1]] = Plotter.Plot(inFile.Get(hname).Clone(),legName=massbinsrev[m+1]+' to '+massbinsrev[m],legType='f',option='hist')
    plots_stack[massbinsrev[m+1]].SetFillColor(colors[int(massbinsrev[m+1])])
    plots_stack[massbinsrev[m+1]].SetLineWidth(0)
    splot.Add(plots_stack[massbinsrev[m+1]].plot)
for m in range(len(massbins)-1):
    c.legend.addLegendEntry(plots_stack[massbins[m]])
c.addMainPlot(splot,addToPlotList=False)
#c.setFrame(0,1e-7,9000,1e7)
splot.setRange(c.logy,1.0e-7,1.0e7)
c.legend.resizeHeight()
c.legend.moveLegend(X=-0.1)
c.cleanup('plots/'+hnamebase+'_MassBinsStack.pdf')
