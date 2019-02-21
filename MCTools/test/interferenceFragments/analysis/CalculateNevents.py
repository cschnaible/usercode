'''
This script calculates effective number of events for specified model, mass, pdf, and integrated luminosity
'''
import math
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-model','--model',default='ZPrimeQ',type=str,help='Which model?')
parser.add_argument('-mass','--mass',default=9000,type=float,help='Which mass?')
parser.add_argument('-pdf','--pdf',default='NNPDF30nlo',type=str,help='Which pdf?')
parser.add_argument('-lumi','--lumi',default=150,type=str,help='Which lumi? (in fb-1)')
args = parser.parse_args()
acc = {
        '120':0.27706,
        '200':0.5399,
        '400':0.70361,
        '800':0.82695,
        '1400':0.89374,
        '2300':0.92955,
        '3500':0.94624,
        '4500':0.95427,
        '6000':0.95676,
        }

print args.model, args.mass, args.pdf
inFile = open('crossSections.data')
for line in inFile:
    cols = line.strip('\n').split()
    if cols[0]=='#': continue
    PDF = cols[0]
    model = cols[1]
    mass = float(cols[2])
    mbin = cols[3]
    xs = float(cols[4])
    xserr = float(cols[6])
    xsunit = cols[7]

    if PDF!=args.pdf or model!=args.model or mass!=args.mass: continue
    print mbin, acc[mbin]*0.9, xs*args.lumi*1000, acc[mbin]*0.9*xs*args.lumi*1000
