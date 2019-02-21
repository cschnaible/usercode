from subprocess import Popen, PIPE, STDOUT
import argparse
import glob
parser = argparse.ArgumentParser(description='Grab XS data from GenXSAnalyzer in CMSSW output')
parser.add_argument('-e','--extra',type=str,default='',help='Extra identifier')
args = parser.parse_args()
EXTRA = '_'+args.extra if args.extra else ''

PDFS = ['NNPDF30nlo']
#PDFS = ['CT14nlo','CT10nlo']
#MODELS = ['ZPrimeSSM','ZPrimePSI','ZPrimeQ','ZPrimeT3L','ZPrimeB-L']
#MODELS = ['ZPrimeQ']#,'ZPrimeLR','ZPrimeR']
MODELS = ['DY']
RESMASSES = ['6000','9000']
#RESMASSES = ['4000','4500','5000','5500','6000','6500','7000','7500','8000']
MASSBINSLOW =  ['120','200','400', '800','1400','2300','3500','4500','6000']
MASSBINSHIGH = ['200','400','800','1400','2300','3500','4500','6000', 'Inf']
linesTmp = []

#line = [PDF, MODEL, RESMASS, MASSBINLOW, XS, +-, XSERR]
#grep "After filter: final cross section = " crab/crab_ZPrimeT3LToEE_ResM4000_M120To200_Interference_13TeV-pythia8_NNPDF30nlo_20181004/results/cmsRun-stdout-1.log
#f = '../submit/crab{EXTRA}/crab_{MODEL}ToEE_ResM{RESMASS}_M{LOW}To{HIGH}_Interference_13TeV-pythia8_{PDF}_*/results/cmsRun-stdout-1.log'
#f = '../submit/crab{EXTRA}/crab_{MODEL}ToEE_M{LOW}To{HIGH}_13TeV-pythia8_{PDF}_*/results/cmsRun-stdout-1.log'
f = '../submit/crab{EXTRA}/crab_{MODEL}ToMuMu_M{LOW}To{HIGH}_13TeV-pythia8_{PDF}_*/results/cmsRun-stdout-1.log'

for PDF in PDFS:
    for MODEL in MODELS:
        #for RESMASS in RESMASSES:
        for LOW,HIGH in zip(MASSBINSLOW,MASSBINSHIGH):
            print f.format(**locals())
            FILE = glob.glob(f.format(**locals()))[0]
            #FILE = f.format(**locals())
            cmd = 'grep \"After filter: final cross section = \" {FILE}'.format(**locals())
            out = Popen(cmd,shell=True,stdout=PIPE,stderr=STDOUT,stdin=PIPE)
            output = out.stdout.read()
            print output.strip('\n')
            XS = output.strip('\n').split()[-4]
            XSERR = output.strip('\n').split()[-2]
            UNIT = output.strip('\n').split()[-1]
            #line = [PDF,MODEL,RESMASS,LOW,XS,'+-',XSERR,UNIT]
            line = [PDF,MODEL,LOW,XS,'+-',XSERR,UNIT]
            linesTmp.append(line)

lines = [' '.join(y.strip() for y in x) for x in linesTmp]
open('crossSection_tmp.data','wt').write('\n'.join(lines))
