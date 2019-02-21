import ROOT as R
import numpy as n
R.PyConfig.IgnoreCommandLineOptions = True
R.gROOT.SetBatch(True)

# Imporant note: any functions that manipulate things based on text size assume that
# the containing pad is wider than it is tall. In this case, the character height is
# obtained as a fraction of the pad height, rather than the pad width. A tall, narrow
# pad may cause unexpected behavior in this regard. All text defaults to 4% of height

# Plot, Legend, and Canvas inherit (or pretend to inherit) from their respective ROOT objects
# So anything one would call on the TH1F inside plot or TLegend or TCanvas can be called
# on the Plot, Legend, or Canvas object themselves.
# Note that Plot does not inherit 

# globalSetStyle function, based on TDRStyle, but more flexible
# This function is called ONCE, changing all of the fixed parameters
# Then setStyle is called, changing all of the variable parameters, once per plot
def globalSetStyle():
    style = R.TStyle('style','Style')

    # inverted black body radiator
    style.SetPalette(56)
    style.SetNumberContours(100)

    # generic line thicknesses
    style.SetLineWidth(1)

    # canvas
    style.SetCanvasBorderMode(0)             # off
    style.SetCanvasColor(R.kWhite)           # white

    # pad
    style.SetPadBorderMode(0)                # off
    style.SetPadColor(R.kWhite)              # white
    style.SetPadGridX(R.kFALSE)              # grid x
    style.SetPadGridY(R.kFALSE)              # grid y
    style.SetGridColor(R.kGray)              # gray
    style.SetGridStyle(3)                    # dotted
    style.SetGridWidth(1)                    # pixels

    # frame
    style.SetFrameBorderMode(0)              # off
    style.SetFrameFillColor(R.kWhite)        # white
    style.SetFrameFillStyle(0)               # hollow
    style.SetFrameLineColor(R.kWhite)        # white
    style.SetFrameLineStyle(1)               # solid
    style.SetFrameLineWidth(0)               # pixels

    # legend
    style.SetLegendBorderSize(0)             # off

    # hist
    style.SetHistLineColor(R.kBlack)         # black
    style.SetHistLineStyle(1)                # solid
    style.SetHistLineWidth(2)                # pixels
    style.SetMarkerStyle(R.kFullDotLarge)    # marker
    style.SetMarkerColor(R.kBlack)           # black
    style.SetEndErrorSize(0)                 # no little lines on errors

    # stats box
    style.SetOptStat(0)                      # off

    # fit box
    style.SetOptFit(1)                       # on
    style.SetStatStyle(0)                    # white
    style.SetStatBorderSize(0)               # default 2

    # title
    style.SetOptTitle(0)                     # off
    style.SetTitleTextColor(R.kBlack)        # black
    style.SetTitleStyle(0)                   # hollow
    style.SetTitleFillColor(R.kWhite)        # white
    style.SetTitleBorderSize(0)              # default 2
    style.SetTitleAlign(22)                  # center top

    # axis titles
    style.SetTitleColor(R.kBlack, 'XYZ')     # black
    style.SetTitleOffset(1,'X')              # default 1
    style.SetTitleOffset(1.25,'Y')           # default 1

    # axis labels
    style.SetLabelColor(R.kBlack, 'XYZ')     # black
    style.SetLabelOffset(0.005,'XYZ')        # default 0.005

    # axis
    style.SetAxisColor(R.kBlack, 'XYZ')      # black
    style.SetStripDecimals(R.kTRUE)          # strip decimals
    style.SetPadTickX(1)                     # opposite x ticks
    style.SetPadTickY(1)                     # opposite y ticks

    style.cd()
globalSetStyle()

# setStyle function, based on TDRStyle, but more flexible
def setStyle(width=800, height=600, font=42, fontsize=0.04):
    style = R.gStyle

    width = width
    height = height
    font = font
    tMargin = 0.1
    lMargin = 0.125
    fontsize = float(fontsize)

    rMargin = tMargin * float(height) / float(width)
    bMargin = lMargin
    titleX = lMargin + (1-lMargin-rMargin)/2
    titleY = 1 - (tMargin/2)

    # canvas
    style.SetCanvasDefW(width)               # width
    style.SetCanvasDefH(height)              # height

    # pad margins
    style.SetPadTopMargin(tMargin)           # default 0.1
    style.SetPadBottomMargin(bMargin)        # default 0.1
    style.SetPadLeftMargin(lMargin)          # default 0.1
    style.SetPadRightMargin(rMargin)         # default 0.1

    # legend
    #style.SetLegendFont(font)                # helvetica normal
    #style.SetLegendTextSize(fontsize)        # default 0

    # title
    style.SetTitleFont(font,'')              # helvetica normal
    style.SetTitleFontSize(fontsize)         # default 0
    style.SetTitleX(titleX)                  # center title horizontally with respect to frame
    style.SetTitleY(titleY)                  # center title vertically within margin

    # axis titles
    style.SetTitleFont(font, 'XYZ')          # helvetica normal
    style.SetTitleSize(fontsize, 'XYZ')      # default 0.02

    # axis labels
    style.SetLabelFont(font, 'XYZ')          # helvetica normal
    style.SetLabelSize(fontsize, 'XYZ')      # default 0.04

    style.cd()

# wrapper for the Set(Get()) idioms, for shifting, scaling, and moving
def GETSET(Object, Attr, Value, Op):
    if Op == '+':
        getattr(Object, 'Set'+Attr)(getattr(Object, 'Get'+Attr)() + float(Value))
    elif Op == '*':
        getattr(Object, 'Set'+Attr)(getattr(Object, 'Get'+Attr)() * float(Value))

def SHIFT(Object, Attr, Value, Axes=None):
    if Axes is None:
        GETSET(Object, Attr, Value, '+')
    else:
        for axis in Axes:
            GETSET(getattr(Object, 'Get'+axis+'axis')(), Attr, Value, '+')

def SCALE(Object, Attr, Value, Axes=None):
    if Axes is None:
        GETSET(Object, Attr, Value, '*')
    else:
        for axis in Axes:
            GETSET(getattr(Object, 'Get'+axis+'axis')(), Attr, Value, '*')

def MOVE_OBJECT(Object, X=0., Y=0., NDC=False):
    EXTRA = '' if not NDC else 'NDC'
    SHIFT(Object, 'X1'+EXTRA, X)
    SHIFT(Object, 'X2'+EXTRA, X)
    SHIFT(Object, 'Y1'+EXTRA, Y)
    SHIFT(Object, 'Y2'+EXTRA, Y)

def MOVE_EDGES(Object, L=0., R=0., T=0., B=0., NDC=False):
    EXTRA = '' if not NDC else 'NDC'
    SHIFT(Object, 'X1'+EXTRA, L)
    SHIFT(Object, 'X2'+EXTRA, R)
    SHIFT(Object, 'Y1'+EXTRA, B)
    SHIFT(Object, 'Y2'+EXTRA, T)

# Enhances a plot object, expected to be a hist, graph, or hstack
# legName is the legend display name, legType is the legend symbol draw option, option is the draw option
class Plot(object):
    def __init__(self, plot, legName='hist', legType='felp', option=''):
        self.plot = plot
        self.legName = legName
        self.legType = legType
        self.option = option
    
    # allows Plot objects to behave as if they were inherited from plot
    def __getattr__(self, name):
        return getattr(self.plot, name)

    # scales axis title sizes
    def scaleTitles(self, factor, axes='XY'):
        SCALE(self, 'TitleSize', float(factor), Axes=axes)

    # scales axis label sizes
    def scaleLabels(self, factor, axes='XY'):
        SCALE(self, 'LabelSize', float(factor), Axes=axes)
    
    # scales axis title offsets from axis
    def scaleTitleOffsets(self, factor, axes='XY'):
        SCALE(self, 'TitleOffset', float(factor), Axes=axes)
    
    # sets axis titles
    def setTitles(self, X=None, Y=None, Z=None):
        for axis,title in zip(('X', 'Y', 'Z'),(X, Y, Z)):
            if title is not None: getattr(self, 'Get'+axis+'axis')().SetTitle(title)

class Stack(object):
    def __init__(self,plot,option=''):
        self.plot = plot
        self.option = option

    def __getattr__(self,name):
        return getattr(self.plot, name)

    # Because ROOT developers are sadists you cannot explicitly set the y-axis range.
    # They want you to lose an afternoon of work before finding this page on the forum:
    # https://root-forum.cern.ch/t/trouble-w-stackhistograms/12390
    # Which explains why you cannot set the range explicitly and instead need to 
    # work around their dumb attempts to "make the plot look nicer" for you.
    # Still, for some reason it is still just ever so slightly not correct
    # even with this work around. Boo.
    def setRange(self,logy,themin,themax):
        if logy:
            ratio = float(themax)/float(themin)
            self.plot.SetMaximum(themax/(1.0+0.2*R.TMath.Log10(ratio)))
            self.plot.SetMinimum(themin*(1.0+0.5*R.TMath.Log10(ratio)))
        else:
            self.plot.SetMaximum(themax/(1.+R.gStyle.GetHistTopMargin()))
            self.plot.SetMinimum(themin)

# Enhances a TLegend, providing some much needed geometry functionality
# X1, X2, Y1, Y2 construct the parent TLegend object; corner is a pos string (see Canvas)
class Legend(R.TLegend):
    def __init__(self, X1, Y1, X2, Y2, corner):
        R.TLegend.__init__(self, X1, Y1, X2, Y2)
        self.lines = 0
        self.corner = corner

    # wrapper for adding legend entries; keeps track of the number of entries
    def addLegendEntry(self, plot):
        self.AddEntry(plot.plot, plot.legName, plot.legType)
        self.lines += 1
    
    # moves the entire legend X, Y units in the x and y directions
    def moveLegend(self, X=0., Y=0.):
        MOVE_OBJECT(self, X=X, Y=Y)
    
    # moves the L, R, T, B edges. Positive is right/up; negative is left/down
    def moveEdges(self, L=0., R=0., T=0., B=0.):
        MOVE_EDGES(self, L=L, R=R, T=T, B=B)
    
    # resizes the legend bounding box based on the number of entries
    # scale allows for some extra padding if desired
    def resizeHeight(self, scale=1.):
        fontsize = self.GetTextSize()
        oldheight = self.GetY2() - self.GetY1()
        newheight = self.lines * fontsize * scale * 1.25
        resize = newheight - oldheight
        # Assume the anchoring corner is in the correct spot
        if self.corner[0] == 't':
            self.moveEdges(B=-resize) # resize > 0 = move B down = negative
        elif self.corner[0] == 'b':
            self.moveEdges(T=resize)  # resize > 0 = move T up   = positive

# Canvas class: enhances a TCanvas by providing several methods for organizing and automating plotting
# cWidth is canvas width, cHeight is canvas height
# fontcode is a string controlling the global font characteristics; see drawText below
# fontscale is a scale factor for resizing globally the font size (defaulting to 0.04 of the height)
# logy is if canvas should be log y scale
# lumi is lumi text (top right), extra is text that follows CMS (top left)
# ratiofactor is fraction of canvas devoted to ratio plot
class Canvas(R.TCanvas):
    def __init__(self, logy=False, lumi='', ratioFactor=0, extra='Internal', cWidth=800, cHeight=600, fontcode='', fontscale=1.):
        self.cWidth      = cWidth
        self.cHeight     = cHeight
        self.fontcode    = fontcode
        self.lumi        = lumi
        self.extra       = extra
        self.logy        = logy
        self.ratioFactor = float(ratioFactor)

        self.legend      = None
        self.plotList    = []
        self.axesDrawn   = False
        self.fontsize    = 0.04

        FontDict = {'' : 4, 'i' : 5, 'b' : 6, 'bi' : 7}
        self.font = 10 * FontDict[fontcode] + 2

        setStyle(self.cWidth,self.cHeight,self.font,self.fontsize*fontscale)

        R.TCanvas.__init__(self, 'c','Canvas',self.cWidth,self.cHeight)

        self.mainPad = R.TPad('main','Main',0,self.ratioFactor,1,1)
        
        if (self.ratioFactor != 0):
            tMargin = self.GetTopMargin()
            lMargin = self.GetLeftMargin()
            rMargin = self.GetRightMargin()

            self.mainPad.SetBottomMargin(0.04)
            self.mainPad.SetRightMargin (tMargin * (self.cHeight * (1 - self.ratioFactor)) / self.cWidth)
            self.ratPad = R.TPad('ratio','Ratio',0,0,1,self.ratioFactor)
            self.ratPad.SetTopMargin(0.04)
            self.ratPad.SetBottomMargin(lMargin * (1 - self.ratioFactor)/self.ratioFactor)
            self.ratPad.SetRightMargin (tMargin * (self.cHeight * (1 - self.ratioFactor)) / self.cWidth)
            self.ratPad.Draw()
            self.ratAxesDrawn = False
            self.ratLegend = None
            self.firstRatioPlot = None
            self.ratList = []

        self.mainPad.Draw()
        self.mainPad.SetLogy(self.logy)

        self.margins = {
            't' : float(self.mainPad.GetTopMargin()),
            'l' : float(self.mainPad.GetLeftMargin()),
            'r' : float(self.mainPad.GetRightMargin()),
            'b' : float(self.mainPad.GetBottomMargin())
        }

    # adds a plot Plot to the main pad
    # the order in which this is called determines the draw order
    # the first plot controls the axes, labels, titles, etc. and is referred to as firstPlot
    # by default, the draw order (stored in plotList) is also used for the legend order
    # just in case, if necessary, addToPlotList=False won't add a plot to plotList
    # addS is for drawing with option 'sames', required for fit boxes
    def addMainPlot(self, plot, addToPlotList=True, addS=False):
        plot.UseCurrentStyle()
        self.cd()
        self.mainPad.cd()
        if addToPlotList: self.plotList.append(plot)

        if not self.axesDrawn:
            self.axesDrawn = True
            self.firstPlot = plot
            if type(plot.plot) in [R.TGraph,R.TGraphErrors,R.TGraphAsymmErrors]:
                plot.Draw('A'+plot.option)
            else:
                plot.Draw(plot.option)
            plot.GetXaxis().CenterTitle()
            plot.GetYaxis().CenterTitle()

            if self.ratioFactor != 0:
                plot.GetXaxis().SetLabelSize(0)
        else:
            if not addS:
                plot.Draw(plot.option+' same')
            else:
                plot.Draw(plot.option+' sames')

    # sets the canvas maximum to 5% above the maximum of all the plots in plotList
    # recompute forces recomputation of the maximum (if it's wrong, for example)
    # cjs - I like 10% above the maximum more
    # cjs - factor above maximum is also changable
    def setMaximum(self, recompute=False,factor=1.1):
        if not recompute:
            self.firstPlot.SetMaximum(factor * max([p.GetMaximum() for p in self.plotList]))
        else:
            realMax = 0.
            for p in self.plotList:
                for ibin in xrange(1, p.GetNbinsX()+1):
                    if p.GetBinContent(ibin) > realMax:
                        realMax = p.GetBinContent(ibin)
            self.firstPlot.SetMaximum(factor * realMax)

    # creates the legend
    # lWidth is width as fraction of pad; height defaults to 0.2, offset defaults to 0.03
    # pos can be tr, tl, br, bl for each of the four corners
    # fontscale is a scale factor for resizing globally the font size (defaulting to 0.04 of the height)
    # autoOrder is if the legend should get its order from the plotList (draw order) or manually
    # if manually, call addLegendEntry on plot objects in the order desired
    def makeLegend(self, lWidth=0.125, pos='tr', fontscale=1., autoOrder=True):
        self.cd()
        self.mainPad.cd()
        xOffset = 0.03
        yOffset = 0.03
        lHeight = 0.2

        X1 = {'r' : 1-self.margins['r']-xOffset-lWidth , 'l' : self.margins['l']+xOffset        }
        X2 = {'r' : 1-self.margins['r']-xOffset        , 'l' : self.margins['l']+xOffset+lWidth }
        Y1 = {'t' : 1-self.margins['t']-yOffset-lHeight, 'b' : self.margins['b']+yOffset        }
        Y2 = {'t' : 1-self.margins['t']-yOffset        , 'b' : self.margins['b']+yOffset+lHeight}

        if pos not in ['tr', 'tl', 'br', 'bl']:
            print 'Invalid legend position string; defaulting to top-right'
            pos = 'tr'

        self.legend = Legend(X1[pos[1]], Y1[pos[0]], X2[pos[1]], Y2[pos[0]], pos)
        self.legend.SetTextSize(fontscale * self.fontsize)
        self.legend.SetFillStyle(0)

        if autoOrder:
            for plot in self.plotList:
                self.addLegendEntry(plot)

    # wrapper for adding legend entries
    def addLegendEntry(self, plot):
        self.legend.addLegendEntry(plot)

    # sets style for the stats box, if there is one
    # owner is the TGraph or TH1 that generated the stats box
    # lWidth is width as fraction of pad, lHeight is height as fraction of pad, lOffset is offset from corner as fraction of pad
    # pos can be tr, tl, br, bl for each of the four corners
    def setFitBoxStyle(self, owner, lWidth=0.3, lHeight=0.15, pos='tl', lOffset=0.05, fontscale=0.75):
        self.cd()
        self.mainPad.cd()
        self.mainPad.Update()

        sbox = owner.FindObject('stats')

        sbox.SetTextFont(self.font)
        sbox.SetTextSize(fontscale * self.fontsize)

        xOffset = 0.03
        yOffset = 0.03

        X1 = {'r' : 1-self.margins['r']-xOffset-lWidth , 'l' : self.margins['l']+xOffset        }
        X2 = {'r' : 1-self.margins['r']-xOffset        , 'l' : self.margins['l']+xOffset+lWidth }
        Y1 = {'t' : 1-self.margins['t']-yOffset-lHeight, 'b' : self.margins['b']+yOffset        }
        Y2 = {'t' : 1-self.margins['t']-yOffset        , 'b' : self.margins['b']+yOffset+lHeight}

        if pos not in ['tr', 'tl', 'br', 'bl']:
            print 'Invalid legend position string; defaulting to top-left'
            pos = 'tl'

        sbox.SetX1NDC(X1[pos[1]])
        sbox.SetX2NDC(X2[pos[1]])
        sbox.SetY1NDC(Y1[pos[0]])
        sbox.SetY2NDC(Y2[pos[0]])

    # makes ratio plot given a top hist and a bottom hist
    # plusminus is the window around 1, i.e. 0.5 means plot from 0.5 to 1.5
    # ytit is the y axis title, xtit is the x axis title, option is the draw option
    # cjs - add an option to make the ratio (a-b)/b ** Removed as of 2 Nov 2018 **
    # cjs - add option to plot multiple ratios on same plot
    # cjs - add option for type of ratio: ratio of poisson means or binomial ratio ** in development **
    def addRatioPlot(self, topPlot, bottomPlot, color=R.kBlack, legName='', legType='pe', option='pe', ytit='Data/MC', xtit='', plusminus=0.5,center=1.,drawLine=True):#, zeroed=False, ratio='poisson'
        if self.ratioFactor == 0: return
        #center = 0. if zeroed else 1.
        #center = 1.
        self.cd()
        self.ratPad.cd()
        self.ratPad.SetGridy(R.kTRUE)
        factor = (1 - self.ratioFactor)/self.ratioFactor

#        if ratio=='poisson':
#            ratGraph, rat, erl, erh = binomial_divide(topPlot.Clone(),bottomPlot.Clone(),confint=clopper_pearson_poisson_means,force_lt_1=False)
#        elif ratio=='binomial':
#            ratGraph, rat, erl, erh = binomial_divide(topPlot.Clone(),bottomPlot.Clone(),confint=clopper_pearson,force_lt_1=True)
#        else:
#            print ratio, 'Not a valid ratio type'
#        self.rat = Plot(ratGraph,legName=legName,legType=legType,option=option)
        ratHist = topPlot.Clone(topPlot.GetName()+'_ratio')
        ratHist.Divide(bottomPlot.plot)
        self.rat = Plot(ratHist,legName=legName,legType=legType,option=option)


#        if zeroed:
#            nbins = rat.GetNbinsX()
#            for ibin in range(1, nbins):
#                f_bin = rat.GetBinContent(ibin)
#                self.rat.SetBinContent(ibin, f_bin-1.)


        if not self.ratAxesDrawn:
            self.firstRatioPlot = self.rat

            if (xtit != ''):
                self.rat.GetXaxis().SetTitle(xtit)
            SCALE(self.rat, 'TitleSize', factor, Axes='XY')
            SCALE(self.rat, 'LabelSize', factor, Axes='XY')
            SCALE(self.rat, 'TickLength', factor, Axes='X')
            self.rat.GetXaxis().CenterTitle()

            self.rat.GetYaxis().SetTitle(ytit)
            SCALE(self.rat, 'TitleOffset', 1./factor, Axes='Y')
            self.rat.GetYaxis().SetTickLength (0.01)
            self.rat.GetYaxis().CenterTitle()
            self.rat.GetYaxis().SetNdivisions(505)
            self.rat.GetYaxis().SetRangeUser(center-plusminus,center+plusminus)
            self.rat.GetXaxis().SetLabelSize(factor*self.fontsize)#, 'XYZ')      # default 0.04
            self.rat.GetYaxis().SetLabelSize(factor*self.fontsize)#, 'XYZ')      # default 0.04

            self.rat.Draw(option)
            self.ratAxesDrawn = True

            if drawLine:
                low = self.rat.GetXaxis().GetXmin()
                up  = self.rat.GetXaxis().GetXmax()
                x   = n.array([ low, up ])
                y   = n.array([ center , center ])
                self.gr = R.TGraph(2,x,y)
                self.gr.SetLineColor(R.kRed)
                self.gr.SetLineStyle(3)
                self.gr.SetLineWidth(2)
                self.gr.Draw('C same')

        self.rat.Draw(option+' same')
        self.rat.SetMarkerColor(color)
        self.rat.SetLineColor(color)
        self.ratPad.RedrawAxis()
        self.ratList.append(self.rat)

    # creates the legend in the ratio plot pad
    # lWidth is width as fraction of pad; height defaults to 0.2, offset defaults to 0.03
    # pos can be tr, tl, br, bl for each of the four corners
    # fontscale is a scale factor for resizing globally the font size (defaulting to 0.04 of the height)
    # fontscale needs to be larger for the ratio legend since default font sice must mean 0.04 of the pad height
    # autoOrder is if the legend should get its order from the plotList (draw order) or manually
    # if manually, call addLegendEntry on plot objects in the order desired
    def makeRatioLegend(self, lWidth=0.125, pos='tr', fontscale=1.5, autoOrder=True):
        self.cd()
        self.ratPad.cd()
        xOffset = 0.03
        yOffset = 0.03
        lHeight = 0.2

        X1 = {'r' : 1-self.margins['r']-xOffset-lWidth , 'l' : self.margins['l']+xOffset        }
        X2 = {'r' : 1-self.margins['r']-xOffset        , 'l' : self.margins['l']+xOffset+lWidth }
        Y1 = {'t' : 1-self.margins['t']-yOffset-lHeight, 'b' : self.margins['b']+yOffset        }
        Y2 = {'t' : 1-self.margins['t']-yOffset        , 'b' : self.margins['b']+yOffset+lHeight}

        if pos not in ['tr', 'tl', 'br', 'bl']:
            print 'Invalid legend position string; defaulting to top-right'
            pos = 'tr'

        self.ratLegend = Legend(X1[pos[1]], Y1[pos[0]], X2[pos[1]], Y2[pos[0]], pos)
        self.ratLegend.SetTextSize(fontscale * self.fontsize)
        self.ratLegend.SetFillStyle(0)

        if autoOrder:
            for rat in self.ratList:
                self.ratLegend.addLegendEntry(rat)

    # makes background transparent
    def makeTransparent(self):
        self.SetFillStyle(4000)
        self.mainPad.SetFillStyle(4000)
        if self.ratioFactor != 0:
            self.ratPad.SetFillStyle(4000)

    # moves exponent away from under CMS
    def moveExponent(self):
        R.TGaxis.SetExponentOffset(-0.08, 0.02, "y")

    # makes an extra axis
    def makeExtraAxis(self, xmin, xmax, Xmin=None, Xmax=None, Ymin=None, Ymax=None, Yoffset=None, Yoffsetscale=0.23, title='', bMarginScale=None):
        self.cd()
        self.mainPad.cd()
        if bMarginScale is None: bMarginScale = 2. if self.ratioFactor == 0. else 2./0.5
        self.scaleMargins(bMarginScale, 'B')
        xaxis = self.firstPlot.GetXaxis()
        if Xmin    is None: Xmin    = xaxis.GetXmin()
        if Xmax    is None: Xmax    = xaxis.GetXmax()
        if Ymin    is None: Ymin    = self.firstPlot.GetMinimum()
        if Ymax    is None: Ymax    = self.firstPlot.GetMaximum()
        if Yoffset is None: Yoffset = (Ymax-Ymin) * Yoffsetscale * (1-self.ratioFactor)
        axis = R.TGaxis(Xmin, Ymin-Yoffset, Xmax, Ymin-Yoffset, xmin, xmax, 510)
        for attr in ('LabelFont', 'LabelOffset', 'TitleFont', 'TitleOffset', 'TitleSize'):
            getattr(axis, 'Set'+attr)(getattr(xaxis, 'Get'+attr)())
        axis.SetLabelSize(xaxis.GetLabelSize() if self.ratioFactor == 0. else self.firstPlot.GetYaxis().GetLabelSize())
        axis.SetTitle    (title)
        axis.CenterTitle()
        axis.Draw()
        return axis

    # scales pad margins
    # factor is the scale factor
    # edges is a string containing a subset of 'LRTB' controlling which margins
    def scaleMargins(self, factor, edges=''):
        EdgeDict = {'L' : 'Left', 'R' : 'Right', 'T' : 'Top', 'B' : 'Bottom'}
        for edge in edges:
            SCALE(self.mainPad, EdgeDict[edge]+'Margin', float(factor))
            self.margins[edge.lower()] = float(getattr(self.mainPad, 'Get'+EdgeDict[edge]+'Margin')())

    # draws some text onto the canvas
    # text is the text
    # pos is a positional tuple in NDC
    # align is a string containing two characters, one each of 'bct' and 'lcr' controlling alignment
    # fontcode is a string containing a subset (including empty) of 'bi' controlling bold, italic
    # NDC is whether or not to use NDC
    def drawText(self, text='', pos=(0., 0.), align='bl', fontcode='', fontscale=1., NDC=True):
        latex = R.TLatex()
        AlignDict = {'l' : 1, 'c' : 2, 'r' : 3, 'b' : 1, 't' : 3}
        FontDict = {'' : 4, 'i' : 5, 'b' : 6, 'bi' : 7}
        RAlign = 10 * AlignDict[align[1]] + AlignDict[align[0]]
        RFont = 10 * FontDict[fontcode] + 2
        latex.SetTextAlign(RAlign)
        latex.SetTextFont(RFont)
        latex.SetTextSize(self.fontsize * fontscale)
        if NDC:
            latex.DrawLatexNDC(pos[0], pos[1], text)
        else:
            latex.DrawLatex(pos[0], pos[1], text)
        return latex

    # makes a stat box, given a ROOT color number
    def makeStatsBox(self, plot, color=1):
        entries = ('mean', 'stddev', 'nentries', 'underflow', 'overflow')
        texts = (
            '{:.4f}'.format(plot.GetMean()),
            '{:.4f}'.format(plot.GetStdDev()),
            '{:.0f}'.format(plot.GetEntries()),
            '{:.0f}'.format(plot.GetBinContent(0)),
            '{:.0f}'.format(plot.GetBinContent(plot.GetNbinsX()+1)),
        )
        names = ('#bar{x}', 's', 'n', 'u', 'o')

        # width = (max length + name + 2 spaces + equals) * an average character width that works
        width = (max([len(t) for t in texts]) + 4)*0.015

        # pave coordinates: 0.03 for offset from frame, len(entries)*self.fontsize is approximately the height
        pave = R.TPaveText(1-self.margins['r']-0.03-width, 1-self.margins['t']-0.03-len(entries)*self.fontsize,
                           1-self.margins['r']-0.03      , 1-self.margins['t']-0.03,
                           'NDCNB'
        )

        # set pave styles: tl, normal, no margin, fill, or border
        pave.SetTextAlign(13)
        pave.SetTextFont(42)
        pave.SetTextSize(self.fontsize*.9)
        pave.SetMargin(0)
        pave.SetFillStyle(0)
        pave.SetFillColor(4000)
        pave.SetLineStyle(0)
        pave.SetLineColor(4000)

        # add all the entries and draw, then move the pave
        for i, (entry, text, name) in enumerate(zip(entries, texts, names)):
            pave.AddText(0., 1.-float(i)/len(entries)-0.1, '#color[{C}]{{{N} = {T}}}'.format(C=color, N=name, T=text))
        pave.Draw()
        MOVE_OBJECT(pave, Y=.08*len(entries)*self.fontsize)

        # make sure you keep a reference to this or the text will disappear
        return pave

    # Draw the frame exactly how you want it
    def setFrame(self,xlo,ylo,xhi,yhi):
        self.cd()
        self.mainPad.cd()
        self.mainPad.DrawFrame(xlo,ylo,xhi,yhi)
        self.mainPad.Modified()
        self.mainPad.Update()
        self.cd()
    
    # draws the lumi text, 'CMS', extra text, and legend 
    def finishCanvas(self, mode='', extrascale=1., drawCMS=True):
        self.makeTransparent()
        self.moveExponent()
        self.cd()
        self.mainPad.cd()
        #self.mainPad.Update()

        tBaseline = 1-self.margins['t']+0.02
        LEFT, RIGHT = self.margins['l'], 1-self.margins['r']

        if mode == '':
            if drawCMS:
                # 'CMS' is approximately 2.75 times wide as tall, so draw extra at 2.75 * charheight to the right of CMS as a fraction of width
                CMSOffset = self.fontsize * self.cHeight * (1-self.ratioFactor) * 2.75 / self.cWidth * extrascale
                self.drawText(text='CMS'     , pos=(LEFT          , tBaseline), align='bl', fontcode='b'          ,fontscale=1.25*extrascale)
                self.drawText(text=self.extra, pos=(LEFT+CMSOffset, tBaseline), align='bl', fontcode='i'          ,fontscale=1.  *extrascale)
                self.drawText(text=self.lumi , pos=(RIGHT         , tBaseline), align='br', fontcode=self.fontcode,fontscale=1.  *extrascale)
            else:
                self.drawText(text=self.extra, pos=(LEFT          , tBaseline), align='bl', fontcode=self.fontcode,fontscale=1.  *extrascale)
                self.drawText(text=self.lumi , pos=(RIGHT         , tBaseline), align='br', fontcode=self.fontcode,fontscale=1.  *extrascale)
        elif mode == 'BOB':
            self    .drawText(text=self.lumi , pos=((RIGHT+LEFT)/2, tBaseline), align='bc', fontcode=self.fontcode,fontscale=1.5 *extrascale)

        if self.legend is not None:
            self.legend.Draw()
        if self.ratioFactor>0 and self.ratLegend is not None:
            self.cd()
            self.ratPad.cd()
            self.ratLegend.Draw()
            self.cd()
            self.mainPad.cd()
        self.mainPad.RedrawAxis()
    
    # saves canvas as file
    def save(self, name, extList=''):
        if type(extList) == str:
            if extList == '':
                self.SaveAs(name)
            else:
                self.SaveAs(name+extList)
        if type(extList) == list:
            for ext in extList:
                self.SaveAs(name+ext)
    
    # deletes the ROOT TCanvas pointer
    # This is to prevent lousy "RuntimeWarning: Deleting canvas with same name: c" errors
    def deleteCanvas(self):
        R.gROOT.ProcessLine('delete gROOT->FindObject("c");')

    # performs a standard finishCanvas, save, and delete
    def cleanup(self, filename, mode=''):
        self.finishCanvas(mode)
        #R.SetOwnership(self, False)
        self.save(filename)
        self.deleteCanvas()


def get_integral(hist, xlo, xhi=None, integral_only=False, include_last_bin=True, nm1=False):
    """For the given histogram, return the integral of the bins
    corresponding to the values xlo to xhi along with its error.

    Edited to return 0 if integral is negative (for N-1 calculation 
    to prevent negative efficeincy when events have negative weights)
    """
    
    binlo = hist.FindBin(xlo)
    if xhi is None:
        binhi = hist.GetNbinsX()+1
    else:
        binhi = hist.FindBin(xhi)
        if not include_last_bin:
            binhi -= 1

    integral = hist.Integral(binlo, binhi)
    if integral_only:
        if nm1 and integral < 0:
            return 0
        else:
            return integral

    wsq = 0
    for i in xrange(binlo, binhi+1):
        wsq += hist.GetBinError(i)**2
    if nm1 and integral < 0:
        return 0,0
    else:
        return integral, wsq**0.5

def poisson_interval(nobs, alpha=(1-0.6827)/2, beta=(1-0.6827)/2):
    lower = 0
    if nobs > 0:
        lower = 0.5 * R.Math.chisquared_quantile_c(1-alpha, 2*nobs)
    elif nobs == 0:
        beta *= 2
    upper = 0.5 * R.Math.chisquared_quantile_c(beta, 2*(nobs+1))
    return lower, upper

def poisson_intervalize(h, zero_x=False, include_zero_bins=False):
    h2 = R.TGraphAsymmErrors(h)
    for i in xrange(1, h.GetNbinsX()+1):
        c = h.GetBinContent(i)
        if c == 0 and not include_zero_bins:
            continue
        l,u = poisson_interval(c)
        # i-1 in the following because ROOT TGraphs count from 0 but
        # TH1s count from 1
        if zero_x:
            h2.SetPointEXlow(i-1, 0)
            h2.SetPointEXhigh(i-1, 0)
        h2.SetPointEYlow(i-1, c-l)
        h2.SetPointEYhigh(i-1, u-c)
    return h2

def clopper_pearson(n_on, n_tot, alpha=1-0.6827, equal_tailed=True):
    if equal_tailed:
        alpha_min = alpha/2
    else:
        alpha_min = alpha

    lower = 0
    upper = 1

    if n_on > 0:
        lower = R.Math.beta_quantile(alpha_min, n_on, n_tot - n_on + 1)
    if n_tot - n_on > 0:
        upper = R.Math.beta_quantile_c(alpha_min, n_on + 1, n_tot - n_on)

    if n_on == 0 and n_tot == 0:
        return 0, lower, upper
    else:
        return float(n_on)/n_tot, lower, upper

def clopper_pearson_poisson_means(x, y, alpha=1-0.6827):
    r, rl, rh = clopper_pearson(x, x+y, alpha)
    print x,y,x/(x+y)
    print r, rl, rh
    print r/(1 - r), rl/(1 - rl), rh/(1 - rh)
    print
    return r/(1 - r), rl/(1 - rl), rh/(1 - rh)

def binomial_divide(h1, h2, confint=clopper_pearson, force_lt_1=True):
    nbins = h1.GetNbinsX()
    xax = h1.GetXaxis()
    if h2.GetNbinsX() != nbins: # or xax2.GetBinLowEdge(1) != xax.GetBinLowEdge(1) or xax2.GetBinLowEdge(nbins) != xax.GetBinLowEdge(nbins):
        raise ValueError, 'incompatible histograms to divide'
    x = []
    y = []
    exl = []
    exh = []
    eyl = []
    eyh = []
    xax = h1.GetXaxis()
    for ibin in xrange(1, nbins+1):
        s,t = h1.GetBinContent(ibin), h2.GetBinContent(ibin)
        if t == 0:
            assert(s == 0)
            continue

        p_hat = float(s)/t
        if s > t and force_lt_1:
            print 'warning: bin %i has p_hat > 1, in interval forcing p_hat = 1' % ibin
            s = t
        rat, a,b = confint(s,t)
        #print ibin, s, t, a, b

        _x  = xax.GetBinCenter(ibin)
        #print "x", _x
        _xw = xax.GetBinWidth(ibin)/2
        #print "xw", _xw
        
        x.append(_x)
        exl.append(_xw)
        exh.append(_xw)

        y.append(p_hat)
        eyl.append(p_hat - a)
        eyh.append(b - p_hat)
    eff = R.TGraphAsymmErrors(len(x), *[array('d', obj) for obj in (x,y,exl,exh,eyl,eyh)])
    return eff, y, eyl, eyh

def core_gaussian(hist, factor, i=[0]):
    core_mean  = hist.GetMean()
    core_width = factor*hist.GetRMS()
    f = R.TF1('core%i' % i[0], 'gaus', core_mean - core_width, core_mean + core_width)
    i[0] += 1
    return f

def cumulative_histogram(h, type='ge'):
    """Construct the cumulative histogram in which the value of each
    bin is the tail integral of the given histogram.
    """
    
    nb = h.GetNbinsX()
    hc = R.TH1F(h.GetName() + '_cumulative_' + type, '', nb, h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax())
    hc.Sumw2()
    if type == 'ge':
        first, last, step = nb+1, 0, -1
    elif type == 'le':
        first, last, step = 0, nb+1, 1
    else:
        raise ValueError('type %s not recognized' % type)
    for i in xrange(first, last, step):
        prev = 0 if i == first else hc.GetBinContent(i-step)
        c = h.GetBinContent(i) + prev
        hc.SetBinContent(i, c)
        if c > 0:
            hc.SetBinError(i, c**0.5)
        else:
            hc.SetBinError(i, 0.)
    return hc

def detree(t, branches='run:lumi:event', cut='', xform=lambda x: tuple(int(y) for y in x)):
    """Dump specified branches from tree into a list of tuples, via an
    ascii file. By default all vars are converted into integers. The
    xform parameter specifies the function transforming the tuple of
    strings into the desired format."""
    
    tmp_fn = os.tmpnam()
    t.GetPlayer().SetScanRedirect(True)
    t.GetPlayer().SetScanFileName(tmp_fn)
    t.Scan(branches, cut, 'colsize=50')
    t.GetPlayer().SetScanRedirect(False)
    l = len(branches.split(':')) + 2
    for line in open(tmp_fn):
        if ' * ' in line and 'Row' not in line:
            yield xform(line.split('*')[2:l])

def draw_in_order(hists, draw_cmds=''):
    hists = [(h, h.GetMaximum()) for h in hists]
    hists.sort(key=lambda x: x[1], reverse=True)
    for h,m in hists:
        print draw_cmds
        h.Draw(draw_cmds)
        if 'same' not in draw_cmds:
            draw_cmds += ' same'

def fit_gaussian(hist, factor=None, draw=False, cache=[]):
    """Fit a Gaussian to the histogram, and return a dict with fitted
    parameters and errors. If factor is supplied, fit only to range in
    hist.mean +/- factor * hist.rms.
    """

    if draw:
        opt = 'qr'
    else:
        opt = 'qr0'

    if factor is not None:
        fcn = core_gaussian(hist, factor)
        cache.append(fcn)
        hist.Fit(fcn, opt)
    else:
        hist.Fit('gaus', opt)
        fcn = hist.GetFunction('gaus')
        
    return {
        'constant': (fcn.GetParameter(0), fcn.GetParError(0)),
        'mu':       (fcn.GetParameter(1), fcn.GetParError(1)),
        'sigma':    (fcn.GetParameter(2), fcn.GetParError(2))
        }
    
def get_bin_content_error(hist, value):
    """For the given histogram, find the bin corresponding to the
    value and return its contents and associated
    error. Multi-dimensional histograms are supported; value may be a
    tuple in those cases.
    """

    if type(value) != type(()):
        value = (value,)
    bin = hist.FindBin(*value)
    return (hist.GetBinContent(bin), hist.GetBinError(bin))

def get_integral(hist, xlo, xhi=None, integral_only=False, include_last_bin=True, nm1=False):
    """For the given histogram, return the integral of the bins
    corresponding to the values xlo to xhi along with its error.

    Edited to return 0 if integral is negative (for N-1 calculation 
    to prevent negative efficeincy when events have negative weights)
    """
    
    binlo = hist.FindBin(xlo)
    if xhi is None:
        binhi = hist.GetNbinsX()+1
    else:
        binhi = hist.FindBin(xhi)
        if not include_last_bin:
            binhi -= 1

    integral = hist.Integral(binlo, binhi)
    if integral_only:
        if nm1 and integral < 0:
            return 0
        else:
            return integral

    wsq = 0
    for i in xrange(binlo, binhi+1):
        wsq += hist.GetBinError(i)**2
    if nm1 and integral < 0:
        return 0,0
    else:
        return integral, wsq**0.5

def get_hist_stats(hist, factor=None, draw=False):
    """For the given histogram, return a five-tuple of the number of
    entries, the underflow and overflow counts, the fitted sigma
    (using the function specified by fcnname, which must be an
    already-made ROOT.TF1 whose parameter(2) is the value used), and the
    RMS.
    """
    
    results = fit_gaussian(hist, factor, draw)
    results.update({
        'entries': hist.GetEntries(),
        'under':   hist.GetBinContent(0),
        'over':    hist.GetBinContent(hist.GetNbinsX()+1),
        'mean':    (hist.GetMean(), hist.GetMeanError()),
        'rms':     (hist.GetRMS(), hist.GetRMSError())
        })
    return results

def make_rms_hist(prof, name='', bins=None, cache={}):
    """Takes an input TProfile and produces a histogram whose bin contents are
    the RMS of the bins of the profile. Caches the histogram so that it doesn't
    get deleted by python before it gets finalized onto a TCanvas.

    If bins is a list of bin lower edges + last bin high edge,
    rebinning is done before making the RMS histogram. Due to a bug in
    ROOT's TProfile in versions less than 5.22 (?), rebinning is done
    manually here.
    """
    
    nbins = prof.GetNbinsX()
    if name == '':
        name = 'RMS' + prof.GetName()
    title = 'RMS ' + prof.GetTitle()
    old_axis = prof.GetXaxis()

    # Play nice with same-name histograms that were OK because they
    # were originally in different directories.
    while cache.has_key(name):
        name += '1'

    # Format of contents list: [(new_bin, (new_bin_content, new_bin_error)), ...]
    contents = []
    
    if bins:
        if type(bins) == type([]):
            bins = array('f', bins)
        new_hist = R.TH1F(name, title, len(bins)-1, bins)
        new_axis = new_hist.GetXaxis()
        new_bins = {}
        for old_bin in xrange(1, nbins+1):
            new_bin = new_axis.FindBin(old_axis.GetBinLowEdge(old_bin))
            if not new_bins.has_key(new_bin):
                new_bins[new_bin] = [0., 0.]
            N = prof.GetBinEntries(old_bin)
            new_bins[new_bin][0] += N*prof.GetBinContent(old_bin)
            new_bins[new_bin][1] += N
        for val in new_bins.values():
            if val[1] > 0:
                val[0] /= val[1]
        contents = new_bins.items()
    else:
        new_hist = R.TH1F(name, title, nbins, old_axis.GetXmin(), old_axis.GetXmax())
        for old_bin in xrange(1, nbins+1):
            f_bin = float(prof.GetBinContent(old_bin))
            ent_bin = float(prof.GetBinEntries(old_bin))
            contents.append((old_bin, (f_bin, ent_bin)))

    for new_bin, (f_bin, ent_bin) in contents:
        if f_bin > 0:
            f_bin = f_bin**0.5
        else:
            f_bin = 0
            
        if ent_bin > 0:
            err_bin = f_bin/(2.*ent_bin)**0.5
        else:
            err_bin = 0

        new_hist.SetBinContent(new_bin, f_bin)
        new_hist.SetBinError(new_bin, err_bin)
        
    cache[name] = new_hist
    return new_hist

def move_below_into_bin(h,a):
    """Given the TH1 h, add the contents of the bins below the one
    corresponding to a into that bin, and zero the bins below."""
    assert(h.Class().GetName().startswith('TH1')) # i bet there's a better way to do this...
    b = h.FindBin(a)
    bc = h.GetBinContent(b)
    bcv = h.GetBinError(b)**2
    for nb in xrange(0, b):
        bc += h.GetBinContent(nb)
        bcv += h.GetBinError(nb)**2
        h.SetBinContent(nb, 0)
        h.SetBinError(nb, 0)
    h.SetBinContent(b, bc)
    h.SetBinError(b, bcv**0.5)

def move_above_into_bin(h,a):
    """Given the TH1 h, add the contents of the bins above the one
    corresponding to a into that bin, and zero the bins above."""
    assert(h.Class().GetName().startswith('TH1')) # i bet there's a better way to do this...
    b = h.FindBin(a)
    bc = h.GetBinContent(b)
    bcv = h.GetBinError(b)**2
    for nb in xrange(b+1, h.GetNbinsX()+2):
        bc += h.GetBinContent(nb)
        bcv += h.GetBinError(nb)**2
        h.SetBinContent(nb, 0)
        h.SetBinError(nb, 0)
    h.SetBinContent(b, bc)
    h.SetBinError(b, bcv**0.5)

def move_overflow_into_last_bin(h):
    """Given the TH1 h, Add the contents of the overflow bin into the
    last bin, and zero the overflow bin."""
    assert(h.Class().GetName().startswith('TH1')) # i bet there's a better way to do this...
    nb = h.GetNbinsX()
    h.SetBinContent(nb, h.GetBinContent(nb) + h.GetBinContent(nb+1))
    h.SetBinError(nb, (h.GetBinError(nb)**2 + h.GetBinError(nb+1)**2)**0.5)
    h.SetBinContent(nb+1, 0)
    h.SetBinError(nb+1, 0)

