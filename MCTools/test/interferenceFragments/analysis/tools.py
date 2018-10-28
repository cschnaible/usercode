#!/usr/bin/env python

import sys, os, glob, math
import ROOT as R
just_testing = 'testing' in sys.argv
if just_testing:
    sys.argv.remove('testing')

try:
    cmd, extra = sys.argv[1].lower(), sys.argv[2:]
except IndexError:
    print 'usage: utils.py command [extra]'
    sys.exit(1)

def do(cmd):
    print cmd
    ret = []
    if not just_testing:
        cmds = cmd.split('\n') if '\n' in cmd else [cmd]
        for cmd in cmds:
            if cmd != '' and not cmd.startswith('#'):
                ret.append(os.system(cmd))
    if len(ret) == 1:
        ret = ret[0]
    return ret

if cmd=='status':
    print cmd
    extra = extra[0] if extra else ''
    for pdf in ['NNPDF30nlo']:#:,'CT10nlo','CT14nlo']:
        for model in ['ZPrimeT3L','ZPrimeQ','ZPrimePSI','ZPrimeSSM']:
            dirs = glob.glob('crab/*_%s*%s_%s'%(model,pdf,extra))
            for d in dirs:
                print d
                do('crab status %s'%d)
if cmd=='getoutput':
    print cmd
    extra = extra[0] if extra else ''
    for pdf in ['NNPDF30nlo']:#:,'CT10nlo','CT14nlo']:
        for model in ['ZPrimeT3L','ZPrimeQ','ZPrimePSI','ZPrimeSSM']:
            dirs = glob.glob('crab/*_%s*%s_%s'%(model,pdf,extra))
            for d in dirs:
                print d
                do('crab getoutput %s'%d)

def printStats(hist):
    print '\n',hist.GetName()
    entries = ('mean', 'stddev', 'nentries', 'underflow', 'overflow')
    texts = (
        '{:.4f}'.format(hist.GetMean()),
        '{:.4f}'.format(hist.GetStdDev()),
        '{:.0f}'.format(hist.GetEntries()),
        '{:.0f}'.format(hist.GetBinContent(0)),
        '{:.0f}'.format(hist.GetBinContent(hist.GetNbinsX()+1)),
    )
    for stat,val in zip(entries,texts):
        print '{0} : {1}'.format(stat,val)


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

class gaus(R.TF1):
    def __init__(self,name,N,mu,sig,lo,hi):
        #eqn ='[0]/TMath::Sqrt(2*TMath::Pi()*'+str(sig)+')*exp(-0.5*((x-'+str(mu)+')/'+str(sig)+')**2)'
        #R.TF1.__init__(self,name,eqn,lo,hi)
        #R.TF1.__init__(self,name,'[0]/TMath::Sqrt(2*TMath::Pi()*[2])*exp(-0.5*((x-[1])/[2])**2)',lo,hi)
        R.TF1.__init__(self,name,'gaus',lo,hi)
        self.SetParameter(0,N)
        self.SetParameter(1,mu)
        self.SetParameter(2,sig)

def get_f_and_pz_values(hist,val,hyp):
    ''' Assume that histogram data is normally distributed, calculate
    RH tail p-values and corresponding conversion to number of sigma (Z-value)
    Returns fitted function, p-value, z-value'''

    f = gaus(hist.GetName()+'_gaus',hist.GetEntries(),hist.GetMean(),hist.GetRMS(),hist.GetXaxis().GetXmin(),hist.GetXaxis().GetXmax())
    hist.Fit(f.GetName(),'NO')
    if hyp=='alt':
        p = f.Integral(val,hist.GetXaxis().GetXmax())/f.Integral(hist.GetXaxis().GetXmin(),hist.GetXaxis().GetXmax())
    elif hyp=='null':
        p = f.Integral(hist.GetXaxis().GetXmin(),val)/f.Integral(hist.GetXaxis().GetXmin(),hist.GetXaxis().GetXmax())
    else:
        print hyp,'not a valid hypothesis type'
        return False,False,False
    
    if float(p) < 0 or float(p) > 1.0: 
        print '\n','*'*45,'\n'
        print hist.GetName()
        print val, f.GetMaximumX()
        print f.Integral(val,f.GetMaximumX()), f.Integral(f.GetMinimumX(),f.GetMaximumX()), p
        print '\n','*'*45,'\n'
    z = math.sqrt(2)*R.TMath.ErfInverse(1 - 2*p)
    return f,p,z
