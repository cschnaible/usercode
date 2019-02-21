#!/usr/bin/env python

import sys, os, glob
import ROOT as R
from subprocess import Popen, PIPE, STDOUT
import argparse
parser = argparse.ArgumentParser(description='Arguments for helper scripts')
parser.add_argument('-c','--crab',default=None,type=str,help='CRAB commands')
parser.add_argument('-e','--extra',default=None,type=str,help='Extra input for CRAB commands')
parser.add_argument('-t','--test',action='store_true',help='Flag for testing')
args = parser.parse_args()

def do(cmd):
    print cmd
    ret = []
    if not args.test:
        cmds = cmd.split('\n') if '\n' in cmd else [cmd]
        for cmd in cmds:
            if cmd != '' and not cmd.startswith('#'):
                ret.append(os.system(cmd))
    if len(ret) == 1:
        ret = ret[0]
    return ret

if args.crab in ['status','getoutput','getlog','report','kill','remake','resubmit','purge']:
    print args.crab
    for pdf in ['CT10nlo','CT14nlo']:#['NNPDF30nlo']:
        for model in ['ZPrimeQ']:
            for mass in ['6000','9000']:
                dirs = glob.glob('crab_20181010/crab_%sToEE_ResM%s_*_%s_%s'%(model,mass,pdf,args.extra))
                for d in dirs:
                    print d
                    do('crab %s -d %s'%(args.crab,d))
                    print '\n','*'*45,'\n'

if args.crab=='status-resubmit':
    for pdf in ['NNPDF30nlo']:#['CT10nlo','CT14nlo']:
        for model in ['ZPrimeT3L']:
            for mass in ['9000','10000','11000','12000','13000']:
                dirs = glob.glob('crab_20181010/*_%sToEE_ResM%s*%s_%s'%(model,mass,pdf,args.extra))
                for d in dirs:
                    print args.crab,d
                    cmd = 'crab status '+d
                    out = Popen(cmd,shell=True,stdout=PIPE,stdin=PIPE,stderr=STDOUT)
                    output = out.stdout.read()
                    print output
                    lines = output.split('\n')
                    doStuff = False
                    for line in lines:
                        if 'Job status:' and 'failed' in line:
                            doStuff = True
                            break
                    if doStuff:
                        print '\n','-'*45,'\n'
                        do('crab resubmit %s'%(d))
                    print '\n','*'*45,'\n'

if args.crab=='status-getoutput-getlog':
    for pdf in ['NNPDF30nlo']:#['CT10nlo','CT14nlo']:
        for model in ['DY']:
            #for mass in ['6000','9000']:
            #dirs = glob.glob('crab_20181010/*_%sToEE_ResM%s_*%s_%s'%(model,mass,pdf,args.extra))
            dirs = glob.glob('crab_20181010/*_%sToMuMu_*%s_%s'%(model,pdf,args.extra))
            print dirs
            for d in dirs:
#                print args.crab,d
#                cmd = 'crab status '+d
#                out = Popen(cmd,shell=True,stdout=PIPE,stdin=PIPE,stderr=STDOUT)
#                output = out.stdout.read()
#                print output
#                lines = output.split('\n')
                doStuff = True
                #for line in lines:
                #    if 'Job status:' and 'finished' in line:
                #        doStuff = True
                #        break
                if doStuff:
                    print '\n','-'*45,'\n'
                    do('crab getoutput %s'%(d))
                    print '\n','-'*45,'\n'
                    do('crab getlog %s'%(d))
                print '\n','*'*45,'\n'

unTarLogFilesTmp = \
'''#!/bin/bash
pushd %s/results
tar -xvf cmsRun_1.log.tar.gz
popd
'''
if args.crab=='untar-log':
    for pdf in ['NNPDF30nlo']:#['CT10nlo','CT14nlo']:
        for model in ['DY']:
            dirs = glob.glob('crab_20181010/*_%sToMuMu*%s_%s'%(model,pdf,args.extra))
            for d in dirs:
                print args.crab,d
                unTarLogFiles = unTarLogFilesTmp%(d)
                open('untar_log.sh','wt').write(unTarLogFiles)
                do('bash untar_log.sh')
                print '\n','-'*45,'\n'
                do('ls %s/results'%d)
                print '\n','*'*45,'\n'
    do('rm untar_log.sh')
    print '\n','*'*45,'\n'


if args.crab=='cleanup':
    dirs = glob.glob('crab_%s/*_%s/results'%(args.extra,args.extra))
    for d in dirs:
        do('rm %s/cmsRun-stderr-1.log %s/FrameworkJobReport-1.xml %s/cmsRun_1.log.tar.gz'%(d,d,d))
