'''
Purpose of script is to count the number of generated events for
simulated Z-prime MC samples
- CMS acceptance
- Barrel-Barrel
- Barrel-Endcap
- Endcap-Endcap
- With and without pT > 53 GeV

Chris Schnaible
30 October 2018
'''
import ROOT as R
import os,glob
import Plotter
R.gROOT.SetBatch(True)
import argparse
parser = argparse.ArgumentParser(description='Options for plotting mass distributions')
parser.add_argument('-id','--indate',default='20181004',type=str,help='Date string for when MC was generated')
parser.add_argument('-c','--crab',default='',type=str,help='Date string for CRAB project directory')
parser.add_argument('-model','--model',default='ZPrimeB-L',type=str,help='Z\' or DY sample, e.g. ZPrimeB-L, ZPrimePSI, or DY')
parser.add_argument('-mass','--mass',default='6000',type=str,help='Resonance mass for Z\' sample')
parser.add_argument('-pdf','--pdf',default='NNPDF30nlo',type=str,help='Loop on PDF sets')
args = parser.parse_args()

if args.indate not in ['20180827','20181001','20181004','20181009','20181010','']:
    print '{DATE} not a correct date string'.format(DATE=args.indate)

DATE = args.indate
CRAB = '_'+args.crab if args.crab else ''
MODEL = args.model
MASS = args.mass if 'ZPrime' in MODEL else '-1'
MASSNAME = '_ResM'+MASS if 'ZPrime' in MODEL else ''
INT = '_Interference' if 'ZPrime' in MODEL else ''
PDF = args.pdf
PDFNAME = '_'+PDF+'_' if PDF in ['NNPDF30nlo','CT14nlo','CT10nlo'] else '_'

# Only generated EE files since gen-level electrons and muons are identical
# Doesn't actually matter either since all the couplings are flavor independent
fileNameTmp = '../submit/crab{CRAB}/crab_{MODEL}ToEE{MASSNAME}_M{LOW}To{HIGH}{INT}_13TeV-pythia8{PDFNAME}*/results/{MODEL}ToEE{MASSNAME}_M{LOW}To{HIGH}{INT}_13TeV-pythia8{PDFNAME}cff_1.root'

MASSBINSLOW  = ['120','200','400', '800','1400','2300','3500','4500','6000']
MASSBINSHIGH = ['200','400','800','1400','2300','3500','4500','6000', 'Inf']



inCMS = '(abs(decay1P4.eta)<2.4 && abs(decay2P4.eta)<2.4)'
etaCuts = {
    'BB':'(abs(decay1P4.eta)<=1.2 && abs(decay2P4.eta)<=1.2)',
    'BE':'(abs(decay1P4.eta)>1.2 || abs(decay2P4.eta)>1.2)',
    'BEee':'((abs(decay1P4.eta)>1.2 && abs(decay2P4.eta)<=1.2) || (abs(decay1P4.eta)<=1.2 && abs(decay2P4.eta)>1.2))',
    'EE':'(abs(decay1P4.eta)>1.2 && abs(decay2P4.eta)>1.2)',
    'inCMS':'1',
    }
ptCuts = {
        'all':'1',
        '53':'(decay1P4.pt>53 && decay2P4.pt>53)',
        }

def countEvents(fileName,cuts):
    f = R.TFile(fileName)
    pdfTree = f.Get('pdfTree')
    # Resolution smearing
    # rndm is a random value generated between 0 and 1.. pretty convienient for smearing
    draw = 'bosonP4.mass >> hist'
    N = pdfTree.Draw(draw,cuts,'goff')
    print N,'\n'
    f.Close()

for cat in ['inCMS','BB','BE','EE']:
    for pt in ['all','53']:
        cuts = inCMS+' && '+etaCuts[cat]+' && '+ptCuts[pt]
        for i,(LOW,HIGH) in enumerate(zip(MASSBINSLOW,MASSBINSHIGH)):
            print MODEL, MASS, LOW, HIGH, PDF
            print cat, pt
            inFileName = glob.glob(fileNameTmp.format(**locals()))[0]
            countEvents(inFileName,cuts)
        print '-'*45
print '*'*45
