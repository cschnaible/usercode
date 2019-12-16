import subprocess,os

crabTemplate='''
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = '%(requestName)s_%(dateString)s'
config.General.workArea = 'crab'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = '%(outName)s'

config.Data.outputPrimaryDataset = '%(requestName)s'
config.Data.inputDBS = 'global'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = %(nevents)s
njobs = 1
config.Data.totalUnits = config.Data.unitsPerJob * njobs
config.Data.publication = False
config.Data.publishDBS = 'phys03' 
config.Data.outputDatasetTag = '%(requestName)s'
config.Data.outLFNDirBase = '/store/user/cschnaib/ZPrime/Interference'
 
config.Site.storageSite = "T2_CH_CERN"
'''

# ZPrimeLRToMuMu_ResM7500_M400To800_Interference

masses = [9000]

samples = [
        ( 120,  200,  5000),
        ( 200,  400,  5000),
        ( 400,  800,  5000),
        ( 800, 1400,  5000),
        (1400, 2300,  5000),
        (2300, 3500,  5000),
        (3500, 4500,  5000),
        (4500, 6000,  5000),
        (6000,   -1,  5000)
#        ( 120,  200, 100000),
#        ( 200,  400, 100000),
#        ( 400,  800,  50000),
#        ( 800, 1400,  25000),
#        (1400, 2300,  25000),
#        (2300, 3500,  25000),
#        (3500, 4500,  10000),
#        (4500, 6000,  10000),
#        (6000,   -1,  10000)
        ]
#massBins = [120,200,400,800,1400,2300,3500,4500,6000,-1]

#models = ['ZPrimeQ','ZPrimeSSM','ZPrimePSI','ZPrimeN','ZPrimeSQ','ZPrimeI','ZPrimeEta','ZPrimeChi','ZPrimeR','ZPrimeB-L','ZPrimeLR','ZPrimeY','ZPrimeT3L']
models = ['ZprimeQ']

#decays = {'EE':11,'MuMu':13}
decays = {'MuMu':13}
pdfs = ['NNPDF31nlo_TuneCP3','NNPDF31nnlo_PR_TuneCP5']
dateString = '20190227'
fragmentDir = 'fragments_nnpdf31'

def makeFragment(fragmentDir,fragmentName):
    fragment_txt = open(fragmentDir+'/'+fragmentName).read()
    fragment = open(fragmentName,'w')
    fragment.write(fragment_txt)
    fragment.close()

for pdftouse in pdfs:
    for mass in masses:
        for mlow,mhigh,nevents in samples:
            for model in models:
                for decay, decayN in decays.iteritems():
                    if mhigh==-1:
                        requestName = '%sTo%s_M%d_M-%dToInf_%s_Interference_13TeV-pythia8'%(model,decay,mass,mlow,pdftouse)
                    else:
                        requestName = '%sTo%s_M%d_M-%dTo%d_%s_Interference_13TeV-pythia8'%(model,decay,mass,mlow,mhigh,pdftouse)
                    fragmentName = requestName+'_cff.py'
                    outName = requestName+'_forCRAB_cff.py'
                    makeFragment(fragmentDir,fragmentName)
                    with open('%s'%outName, 'w') as outfile:
                        subprocess.call(['python','runFragment_nnpdf31.py','fragment=%s'%fragmentName,'decay=%s'%decayN],stdout=outfile)

                    crabCfg = crabTemplate%(locals())
                    f = open('crabCfg.py','w')
                    f.write(crabCfg)
                    f.close()
                    print fragmentName
                    print requestName
                    print outName
                    print
                    subprocess.call(['crab','submit','crabCfg.py'])
                    os.system('rm '+fragmentName+' crabCfg.py '+outName+' *.pyc')

#for pdftouse in pdfs:
#    for mass in masses:
#        for model in models:
#            for decay, decayN in decays.iteritems():
#                requestName = '%sTo%s_ResM%d_13TeV-pythia8_%s'%(model,decay,mass,pdftouse)
#                fragmentName = '%sTo%s_ResM%d_13TeV-pythia8_%s_cff.py'%(model,decay,mass,pdftouse)
#                outName = '%sTo%s_ResM%d_13TeV-pythia8_forCRAB_%s_cff.py'%(model,decay,mass,pdftouse)
#                with open('%s'%outName, 'w') as outfile:
#                    subprocess.call(['python','runFragment.py','fragment=%s'%fragmentName,'decay=%s'%decayN],stdout=outfile)
#
#                crabCfg = crabTemplate%(requestName,outName,requestName,requestName)
#                f = open('crabCfg.py','w')
#                f.write(crabCfg)
#                f.close()
#                subprocess.call(['crab','submit','crabCfg.py'])


model = 'DY'
for pdftouse in pdfs:
    for mlow,mhigh,nevents in samples:
        for decay, decayN in decays.iteritems():
            if mhigh==-1:
                requestName = '%sTo%s_M-%dToInf_%s_13TeV-pythia8'%(model,decay,mlow,pdftouse)
            else:
                requestName = '%sTo%s_M-%dTo%d_%s_13TeV-pythia8'%(model,decay,mlow,mhigh,pdftouse)
            fragmentName = requestName+'_cff.py'
            outName = requestName+'_forCRAB_cff.py'
            makeFragment(fragmentDir,fragmentName)
            with open('%s'%outName, 'w') as outfile:
                    subprocess.call(['python','runFragment_nnpdf31.py','fragment=%s'%fragmentName,'decay=%s'%decayN],stdout=outfile)

            crabCfg = crabTemplate%(locals())
            f = open('crabCfg.py','w')
            f.write(crabCfg)
            f.close()
            print fragmentName
            print requestName
            print outName 
            print
            subprocess.call(['crab','submit','crabCfg.py'])
            os.system('rm '+fragmentName+' crabCfg.py '+outName+' *.pyc')

