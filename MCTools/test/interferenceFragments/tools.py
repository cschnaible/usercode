#!/usr/bin/env python

import sys, os, glob
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

if cmd=='checkdata':
    print cmd
    extra = extra[0] if extra else ''
    dirs = glob.glob('crab/*_%s'%extra)
    for d in dirs:
        print d
        do('crab status %s'%d)
if cmd=='getdata':
    print cmd
    extra = extra[0] if extra else ''
    dirs = glob.glob('crab/*_%s'%extra)
    for d in dirs:
        print d
        do('crab getoutput %s'%d)

