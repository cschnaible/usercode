import sys,os
import commands

if __name__=='__main__':
    user = commands.getoutput('echo $USER')
    cmssw_base = commands.getoutput('echo $CMSSW_BASE')
    baseDir = cmssw_base+'/src/usercode/MCTools/test/interferenceFragments/analysis'
    extra = 'batch_2016_2017_20181010'
    NPE = 5

    add2017 = 'true'

    MLOW = 600
    MHIGH = 9000

    PDFS=['NNPDF30nlo']#['CTEQ5L']#['CT14nlo','CT10nlo']

    outDir = baseDir+'/hists/'+extra
    inputDateString = '20181026'

    os.system('mkdir -p '+baseDir+'/sh')
    os.system('mkdir -p '+outDir)

    if not os.path.isdir(outDir):
        print 'Directory',outDir,'does not exist; exiting.'
        exit()
    elif not os.path.isdir(baseDir+'/sh'):
        print 'Directory',baseDir+'/sh','does not exist; exiting.'
        exit()

    # E6  : PSI, Eta, Chi, I, N, SQ
    # GLR : R, B-L, LR, Y
    # GSM : T3L, SSM, Q
    models = ['T3L','Q']
    #masses = ['4000','4500','5000','5500','6000','6500','7000','7500','8000']
    #masses = ['6000','7000','8000']
    masses = ['9000','10000','11000','12000','13000']
    channels = ['MuMu','EE']


    for PDF in PDFS:
        for channel in channels:
            PDFstring=('_'+PDF+'_' if PDF else '_')
            for model in models:
                for mass in masses:
                    cmd = 'root -l -b -q \"MakeToyDistributions.cpp(\\"{model}\\",\\"{channel}\\",\\"{mass}\\",{add2017},{NPE},{MLOW},{MHIGH},\\"{PDF}\\",\\"{extra}\\",\\"{inputDateString}\\")\"'.format(**locals())
                    if 'dryrun' in sys.argv:
                        print 'Model:',model,PDF
                        print 'Channel:',channel
                        print 'Mass:',mass
                        print cmd
                        print 
                    elif 'submit' in sys.argv:
                        print model, channel, mass, PDF
                        os.system('{cmd}'.format(**locals()))
                        print
