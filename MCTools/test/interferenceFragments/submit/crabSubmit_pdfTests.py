import subprocess

crabTemplate='''
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = '%s_%s'
config.General.workArea = 'crab_%s'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = '%s'

config.Data.outputPrimaryDataset = '%s'
config.Data.inputDBS = 'global'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 100000
config.Data.totalUnits = 100000
config.Data.publication = False
config.Data.publishDBS = 'phys03' 
config.Data.outputDatasetTag = '%s'
config.Data.outLFNDirBase = '/store/user/cschnaib/ZPrime/'
 
config.Site.storageSite = "T2_CH_CERN"
'''

# ZPrimeLRToMuMu_ResM7500_M400To800_Interference

#masses = [1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000]
#masses = [4000,4500,5000,5500,6000,6500,7000,7500,8000]
#masses = [6000]
masses = [9000,10000,11000,12000,13000]

massBins = [120,200,400,800,1400,2300,3500,4500,6000,-1]
#massBins = [4500,6000,-1]

#models = ['ZPrimeQ','ZPrimeSSM','ZPrimePSI','ZPrimeN','ZPrimeSQ','ZPrimeI','ZPrimeEta','ZPrimeChi','ZPrimeR','ZPrimeB-L','ZPrimeLR','ZPrimeY','ZPrimeT3L']
#models = ['ZPrimeQ','ZPrimeSSM','ZPrimeSQ','ZPrimeR','ZPrimeB-L','ZPrimeLR','ZPrimeY','ZPrimeT3L']
#models = ['ZPrimeR','ZPrimeLR','ZPrimeY']
models = ['ZPrimeQ']
#models = ['ZPrimeQ','ZPrimeSSM','ZPrimeT3L','ZPrimePSI','ZPrimeB-L']

decays = {'EE':11}
#decays = {'EE':11,'MuMu':13}
#decays = {'MuMu':13}

pdfs = ['NNPDF30nlo']#'CT10nlo','CT14nlo']
dateString = '20181010'

for pdftouse in pdfs:
	for mass in masses:
		for i in range(0,len(massBins)-1):
			for model in models:
				for decay, decayN in decays.iteritems():
					if massBins[i+1] == -1:
						requestName = '%sTo%s_ResM%d_M%dToInf_Interference_13TeV-pythia8_%s'%(model,decay,mass,massBins[i],pdftouse)
						fragmentName = '%sTo%s_ResM%d_M%dToInf_Interference_13TeV-pythia8_%s_cff.py'%(model,decay,mass,massBins[i],pdftouse)
						outName = '%sTo%s_ResM%d_M%dToInf_Interference_13TeV-pythia8_forCRAB_%s_cff.py'%(model,decay,mass,massBins[i],pdftouse)
					else:
						requestName = '%sTo%s_ResM%d_M%dTo%d_Interference_13TeV-pythia8_%s'%(model,decay,mass,massBins[i],massBins[i+1],pdftouse)
						fragmentName = '%sTo%s_ResM%d_M%dTo%d_Interference_13TeV-pythia8_%s_cff.py'%(model,decay,mass,massBins[i],massBins[i+1],pdftouse)
						outName = '%sTo%s_ResM%d_M%dTo%d_Interference_13TeV-pythia8_forCRAB_%s_cff.py'%(model,decay,mass,massBins[i],massBins[i+1],pdftouse)
					with open('%s'%outName, 'w') as outfile:
						subprocess.call(['python','runFragment.py','fragment=%s'%fragmentName,'decay=%s'%decayN],stdout=outfile)	

					crabCfg = crabTemplate%(requestName,dateString,dateString,outName,requestName,requestName)
					f = open('crabCfg.py','w')
					f.write(crabCfg)
					f.close()
					print fragmentName
					print requestName
					print outName
					print
					subprocess.call(['crab','submit','crabCfg.py'])

exit()
for pdftouse in pdfs:
	for mass in masses:
		for model in models:
			for decay, decayN in decays.iteritems():
				requestName = '%sTo%s_ResM%d_13TeV-pythia8_%s'%(model,decay,mass,pdftouse)
				fragmentName = '%sTo%s_ResM%d_13TeV-pythia8_%s_cff.py'%(model,decay,mass,pdftouse)
				outName = '%sTo%s_ResM%d_13TeV-pythia8_forCRAB_%s_cff.py'%(model,decay,mass,pdftouse)
				with open('%s'%outName, 'w') as outfile:
					subprocess.call(['python','runFragment.py','fragment=%s'%fragmentName,'decay=%s'%decayN],stdout=outfile)

				crabCfg = crabTemplate%(requestName,outName,requestName,requestName)
				f = open('crabCfg.py','w')
				f.write(crabCfg)
				f.close()
				subprocess.call(['crab','submit','crabCfg.py'])


exit()
model = 'DY'
for i in range(0,len(massBins)-1):
	for decay, decayN in decays.iteritems():
		if massBins[i+1] == -1:
			requestName = '%sTo%s_M%dToInf_13TeV-pythia8_%s'%(model,decay,massBins[i],pdftouse)
			fragmentName = '%sTo%s_M%dToInf_13TeV-pythia8_%s_cff.py'%(model,decay,massBins[i],pdftouse)
			outName = '%sTo%s_M%dToInf_13TeV-pythia8_forCRAB_%s_cff.py'%(model,decay,massBins[i],pdftouse)
		else:
			requestName = '%sTo%s_M%dTo%d_13TeV-pythia8_%s'%(model,decay,massBins[i],massBins[i+1],pdftouse)
			fragmentName = '%sTo%s_M%dTo%d_13TeV-pythia8_%s_cff.py'%(model,decay,massBins[i],massBins[i+1],pdftouse)
			outName = '%sTo%s_M%dTo%d_13TeV-pythia8_forCRAB_%s_cff.py'%(model,decay,massBins[i],massBins[i+1],pdftouse)
		with open('%s'%outName, 'w') as outfile:
				subprocess.call(['python','runFragment.py','fragment=%s'%fragmentName,'decay=%s'%decayN],stdout=outfile)	

		crabCfg = crabTemplate%(requestName,outName,requestName,requestName)
		f = open('crabCfg.py','w')
		f.write(crabCfg)
		f.close()
		subprocess.call(['crab','submit','crabCfg.py'])

