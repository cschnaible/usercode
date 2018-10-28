import ROOT as R
import os,glob
import Plotter
R.gROOT.SetBatch(True)
import argparse
parser = argparse.ArgumentParser(description='Options for plotting mass distributions')
parser.add_argument('-out','--outname',default='',type=str,help='Extra name to add to output')
parser.add_argument('-id','--indate',default='20181004',type=str,help='Date string for when MC was generated')
parser.add_argument('-c','--crab',default='',type=str,help='Date string for CRAB project directory')
parser.add_argument('-model','--model',default='ZPrimeB-L',type=str,help='Z\' or DY sample, e.g. ZPrimeB-L, ZPrimePSI, or DY')
parser.add_argument('-mass','--mass',default='6000',type=str,help='Resonance mass for Z\' sample')
parser.add_argument('-pdf','--pdf',default='NNPDF30nlo',type=str,help='Loop on PDF sets')
args = parser.parse_args()

if args.indate not in ['20180827','20181001','20181004','20181009','20181010','']:
    print '{DATE} not a correct date string'.format(DATE=args.indate)

OUTNAME = args.outname
DATE = args.indate
CRAB = '_'+args.crab if args.crab else ''
MODEL = args.model
MASS = args.mass if 'ZPrime' in MODEL else '-1'
MASSNAME = '_ResM'+MASS if 'ZPrime' in MODEL else ''
INT = '_Interference' if 'ZPrime' in MODEL else ''
PDF = args.pdf
PDFNAME = '_'+PDF+'_' if PDF in ['NNPDF30nlo','CT14nlo','CT10nlo'] else '_'

HNAMETMP = MODEL+'To{CHAN}'+('_ResM'+args.mass if 'ZPrime' in MODEL else '')
FULLHNAMETMP = HNAMETMP+('_Int' if 'ZPrime' in MODEL else '')+'_'+PDF

LUMI = 36300.+42100.


# Only generated EE files since gen-level electrons and muons are identical
# Doesn't actually matter either since all the couplings are flavor independent
fileNameTmp = '../submit/crab{CRAB}/crab_{MODEL}ToEE{MASSNAME}_M{LOW}To{HIGH}{INT}_13TeV-pythia8{PDFNAME}*/results/{MODEL}ToEE{MASSNAME}_M{LOW}To{HIGH}{INT}_13TeV-pythia8{PDFNAME}cff_1.root'

CHANNELS = ['EE','MuMu','LL']#,'GenMuMu']
MASSBINSLOW  = ['120','200','400', '800','1400','2300','3500','4500','6000']
MASSBINSHIGH = ['200','400','800','1400','2300','3500','4500','6000', 'Inf']


outFile = R.TFile.Open('root/ZprimeInterferenceHists_'+MODEL+('_'+args.mass if 'ZPrime' in MODEL else '')+'_'+PDF+('_'+args.outname if args.outname else '')+'.root','recreate')

def sigma(chan):
    BB = '(abs(decay1P4.eta)<=1.2 && abs(decay2P4.eta)<=1.2)'
    BE = '(abs(decay1P4.eta)>1.2 || abs(decay2P4.eta)>1.2)'
    BEee = '((abs(decay1P4.eta)>1.2 && abs(decay2P4.eta)<=1.2) || (abs(decay1P4.eta)<=1.2 && abs(decay2P4.eta)>1.2))'
    if chan=='EE':
        sigmaBB = '(sqrt((pow(10.3,2)/bosonP4.mass)+pow(10.0/bosonP4.mass,2)+pow(0.87,2))+5.6e-5*bosonP4.mass)'
        sigmaBE = 'sqrt((pow(14.5,2)/bosonP4.mass)+pow(10.0/bosonP4.mass,2)+pow(1.49,2))'
        # EE function is defined in terms of %, needs a factor of 0.01
        sigma = '0.01*bosonP4.mass * ({BB}*{sigmaBB} + {BEee}*{sigmaBE})'.format(**locals())
        return sigma

    elif chan=='MuMu':
        sigmaBB_low = '(0.00701+3.32e-5*bosonP4.mass-1.29e-8*pow(bosonP4.mass,2)+2.73e-12*pow(bosonP4.mass,3)-2.05e-16*pow(bosonP4.mass,4))'
        sigmaBB_high = '(0.02475125 + bosonP4.mass*7.809375E-6)'

        sigmaBE_low = '(0.0142+3.75e-5*bosonP4.mass-1.52e-8*pow(bosonP4.mass,2)+3.44e-12*pow(bosonP4.mass,3)-2.85e-16*pow(bosonP4.mass,4))'
        sigmaBE_high = '(0.03504625 + bosonP4.mass*8.156875E-6)'

        mLow = '(bosonP4.mass<=4500)'
        mHigh = '(bosonP4.mass>4500)'
        sigma = 'bosonP4.mass*( {BB}*{mLow}*{sigmaBB_low} + {BB}*{mHigh}*{sigmaBB_high} + {BE}*{mLow}*{sigmaBE_low} + {BE}*{mHigh}*{sigmaBE_high} )'.format(**locals())
        return sigma

    elif chan=='LL':
        return '0.'

    else:
        print 'lol'
        exit()

def eff(chan):
    BB = '(abs(decay1P4.eta)<=1.2 && abs(decay2P4.eta)<=1.2)'
    BE = '(abs(decay1P4.eta)>1.2 || abs(decay2P4.eta)>1.2)'
    BEee = '((abs(decay1P4.eta)>1.2 && abs(decay2P4.eta)<=1.2) || (abs(decay1P4.eta)<=1.2 && abs(decay2P4.eta)>1.2))'
    EEee = '(abs(decay1P4.eta)>1.2 && abs(decay2P4.eta)>1.2)'
    inCMS = '(abs(decay1P4.eta)<2.4 && abs(decay2P4.eta)<2.4)'
    if chan=='EE':
        ee_eff_bb = '(0.6484-500.3/(bosonP4.mass+362.3)+6.863e4/(pow(bosonP4.mass,2)+1.209e5))'
        ee_eff_be = '(-0.03434+739/(bosonP4.mass+1260.)-9.172e4/(pow(bosonP4.mass,2)+7.39e4)+1.412e7/(pow(bosonP4.mass,3)+2.185e7))'
        ee_eff_ee = '(0.)'
        ee_eff = '{inCMS}*({BB}*{ee_eff_bb} + {BEee}*{ee_eff_be} + {EEee}*{ee_eff_ee})'.format(**locals())
        return ee_eff
        #return '((abs(decay1P4.eta)<=1.2 && abs(decay2P4.eta)<=1.2)*(0.6484-500.5/(bosonP4.mass+362.3)+6.863e4/(pow(bosonP4.mass,2)+1.209e5)) + (abs(decay1P4.eta)>1.2 || abs(decay2P4.eta)>1.2)*(-0.03434+739/(bosonP4.mass+1260.)-9.172e4/(pow(bosonP4.mass,2)+7.39e4)+1.412e7/(pow(bosonP4.mass,3)+2.185e7)))'
    elif chan=='MuMu':
        m_bb_low = '(bosonP4.mass<600)'
        m_bb_high = '(bosonP4.mass>=600)'
        m_be_low = '(bosonP4.mass<450)'
        m_be_high = '(bosonP4.mass>=450)'
        mm_eff_bb_low = '(2.129-0.1268*exp(-1*(bosonP4.mass-119.2)/22.35)-2.386*pow(bosonP4.mass,-0.03619))'
        mm_eff_bb_high = '(2.891-(2.291e4/(bosonP4.mass+8294.)-0.0001247*bosonP4.mass))'
        mm_eff_be_low = '(13.56-6.672*exp((bosonP4.mass+4.879e6)/7.233e6)-826.0*pow(bosonP4.mass,-1.567))'
        mm_eff_be_high = '(0.2529+0.06511*pow(bosonP4.mass,0.8755)*exp(-1*(bosonP4.mass+4601)/1147.0))'
        mm_eff = '{inCMS}*({BB}*{m_bb_low}*{mm_eff_bb_low} + {BB}*{m_bb_high}*{mm_eff_bb_high} + {BE}*{m_be_low}*{mm_eff_be_low} + {BE}*{m_be_high}*{mm_eff_be_high})'.format(**locals())
        return mm_eff
        #return '((abs(decay1P4.eta)<=1.2 && abs(decay2P4.eta)<=1.2)*((bosonP4.mass>=120 && bosonP4.mass<600)*(2.129-0.1268*exp(-1*(bosonP4.mass-119.2)/22.35)-2.386*pow(bosonP4.mass,-0.03619)) + (bosonP4.mass>=600)*(2.891-(2.291e4/(bosonP4.mass+8294.)-0.0001247*bosonP4.mass))) + (abs(decay1P4.eta)>1.2 || abs(decay2P4.eta)>1.2)*((bosonP4.mass>=120 && bosonP4.mass<450)*(13.56-6.672*exp((bosonP4.mass+4.879e6)/7.233e6)-826.0*pow(bosonP4.mass,-1.567)) + (bosonP4.mass>=450)*(0.2529+0.06511*pow(bosonP4.mass,0.8755)*exp(-1*(bosonP4.mass+4601)/1147.0))))'

    #if 'Gen' in chan: return '1.'
    elif chan=='LL': 
        #return '{inCMS}'.format(**locals())
        return '1.'
    else: 
        print 'lol'
        exit()

XSPDFS = ['NNPDF30nlo','CT10nlo','CT14nlo']
XSMODELS = ['ZPrimeQ','ZPrimeB-L','ZPrimePSI','ZPrimeT3L','ZPrimeSSM','ZPrimeLR','ZPrimeR','ZPrimeY']
RESMASSES = ['4000','4500','5000','5500','6000','6500','7000','7500','8000','9000','10000','11000','12000','13000']
XSTABLE = {pdf:{zp:{resmass:{massbin:{'XS':{},'XSerr':{}} for massbin in ['-1']+MASSBINSLOW} for resmass in RESMASSES} for zp in XSMODELS} for pdf in XSPDFS}
DYXSTABLE = {pdf:{'DY':{'-1':{massbin:{'XS':{},'XSerr':{}} for massbin in MASSBINSLOW}}} for pdf in XSPDFS}
with open("crossSections.data") as xsdata:
    for l,line in enumerate(xsdata):
        data = line.strip('\n').split()
        if data[0]=='#': continue
        pdf = data[0]
        zp = data[1]
        resmass = data[2]
        massbin = data[3]
        xs = float(data[4])
        xserr = float(data[6])
        if zp=='DY':
            DYXSTABLE[pdf][zp][resmass][massbin] = {}
            DYXSTABLE[pdf][zp][resmass][massbin]['XS'] = xs
            DYXSTABLE[pdf][zp][resmass][massbin]['XSerr'] = xserr
        else:
            XSTABLE[pdf][zp][resmass][massbin] = {}
            XSTABLE[pdf][zp][resmass][massbin]['XS'] = xs
            XSTABLE[pdf][zp][resmass][massbin]['XSerr'] = xserr

# Ad-hoc scalings for CTEQ5L PDF set
ALLPDFS = ['CTEQ5L']
ALLMODELS = ['ZPrimeB-L','ZPrimeSSM','ZPrimeQ','ZPrimeR','ZPrimeLR','ZPrimeY','ZPrimeT3L','ZPrimePSI']
ALLRESMASSES = ['4000','4500','5000','5500','6000','6500','7000','7500','8000']
SCALE = {pdf:{zp:{mass:{low:{} for low in MASSBINSLOW} for mass in ALLRESMASSES} for zp in ALLMODELS} for pdf in ALLPDFS}
with open("crossSectionScalings.data") as f:
    for l,line in enumerate(f):
        if l==0: continue # first line is column labels
        if line.strip('\n')=='': continue # skip empty lines
        pdf,zp,RESMASS = line.split()[:3]
        for m,low in enumerate(MASSBINSLOW):
            SCALE[pdf][zp][RESMASS][low] = float(eval(line.split()[3:][m]))

hists = {CHAN:{LOW:{} for LOW in MASSBINSLOW} for CHAN in CHANNELS}
def makeHist(hname,fileName,CHAN,PDF,MODEL,MASS,LOW):
        f = R.TFile(fileName)
        hmin,hmax = 0,9000
        binwidth = 50
        nbins = (hmax-hmin)/binwidth
        hists[CHAN][LOW] = R.TH1F(hname,'',nbins,hmin,hmax)
        hists[CHAN][LOW].Sumw2()
        pdfTree = f.Get('pdfTree')
        # Resolution smearing
        # rndm is a random value generated between 0 and 1.. pretty convienient for smearing
        pdfTree.SetAlias('z','sin(2*pi*rndm)*sqrt(-2*log(rndm))')
        draw = 'bosonP4.mass + {SIGMA}*z >> {HISTNAME}'.format(SIGMA=sigma(CHAN),HISTNAME=hname)
        NEVENTS = float(pdfTree.GetEntries())
        if PDF=='CTEQ5L':
            XS = pdfTree.GetUserInfo().FindObject('crossSec').GetVal()
        else:
            if MODEL=='DY':
                XS = DYXSTABLE[PDF][MODEL][MASS][LOW]['XS']
                #XSerr = DYXSTABLE[MODEL][MASS][MASSBIN]['XSerr']
            else:
                XS = XSTABLE[PDF][MODEL][MASS][LOW]['XS']
                #XSerr = XSTABLE[MODEL][MASS][MASSBIN]['XSerr']
        print hname, XS, LUMI, NEVENTS, XS*LUMI/NEVENTS
        weight = '{EFF}*{XS}*{LUMI}/{NEVENTS}'.format(EFF=eff(CHAN),XS=XS,LUMI=LUMI,NEVENTS=NEVENTS)
        option = 'hist'
        #print draw,weight
        pdfTree.Draw(draw,weight,option)
        hists[CHAN][LOW].SetDirectory(0)
        if PDF=='CTEQ5L' and MODEL!='DY':
            hists[CHAN][LOW].Scale(SCALE[PDF][MODEL][MASS][LOW])
        elif PDF=='CTEQ5L' and MODEL=='DY' and LOW=='800':
            hists[CHAN][LOW].Scale(1.07/0.94)
        f.Close()
        outFile.cd()
        print hname
        hists[CHAN][LOW].Write(hname)

for CHAN in CHANNELS:
    hists[CHAN]['sum'] = {}
    for i,(LOW,HIGH) in enumerate(zip(MASSBINSLOW,MASSBINSHIGH)):
        #inFileName = fileNameTmp.format(**locals())
        inFileName = glob.glob(fileNameTmp.format(**locals()))[0]
        HNAME = HNAMETMP.format(**locals())+'_M'+LOW+'To'+HIGH+('_Int' if 'ZPrime' in MODEL else '')+('_'+PDF if PDF else '')
        FULLHNAME = FULLHNAMETMP.format(**locals())
        makeHist(HNAME,inFileName,CHAN,PDF,MODEL,MASS,LOW)
        if i==0:
            hists[CHAN]['sum'] = hists[CHAN][LOW].Clone(FULLHNAME)
        else:
            hists[CHAN]['sum'].Add(hists[CHAN][LOW])
    print FULLHNAME
    print hists[CHAN]['sum'].GetName()
    hists[CHAN]['sum'].Write()
