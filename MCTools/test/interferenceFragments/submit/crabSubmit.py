import subprocess

crabTemplate='''
#from WMCore.Configuration import Configuration
#config = Configuration()
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

#config.section_("General")
config.General.requestName = '%s_20180926'
config.General.workArea = 'crab'
config.General.transferOutputs = True


#config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = '%s'

#config.section_("Data")
config.Data.outputPrimaryDataset = '%s'
config.Data.inputDBS = 'global'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 100000
config.Data.totalUnits = 100000
config.Data.publication = False
config.Data.publishDBS = 'phys03' 
config.Data.outputDatasetTag = '%s'
config.Data.outLFNDirBase = '/store/user/cschnaib/ZPrime/'
 
#config.section_("Site")
config.Site.storageSite = "T2_CH_CERN"

#config.section_("User")
'''


# ZPrimeLRToMuMu_ResM7500_M400To800_Interference
interference = 0 # turns on interference, set to 3 for Z' only and 4 for Z/gamma Drell-Yan
#masses = [1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000]
masses = [4000,4500,5000,5500,6000,6500,7000,7500,8000]
#masses = [7500]
massBins = [120,200,400,800,1400,2300,3500,4500,6000,-1]
#massBins = [400,800]
models = ["ZPrimeQ","ZPrimeSSM","ZPrimePSI","ZPrimeN","ZPrimeSQ","ZPrimeI","ZPrimeEta","ZPrimeChi","ZPrimeR","ZPrimeB-L","ZPrimeLR","ZPrimeY","ZPrimeT3L"]
#models = ["ZPrimeQ","ZPrimeSSM","ZPrimeSQ","ZPrimeR","ZPrimeB-L","ZPrimeLR","ZPrimeY","ZPrimeT3L"]
#models = ['ZPrimeT3L']
#decays = {"EE":11}
decays = {"EE":11,"MuMu":13}
#decays = {"MuMu":13}
if True:
	for mass in masses:
		for i in range(0,len(massBins)-1):
			for model in models:
				for decay, decayN in decays.iteritems():
					if massBins[i+1] == -1:
						requestName = "%sTo%s_ResM%d_M%dToInf_Interference_13TeV-pythia8"%(model,decay,mass,massBins[i])
						fragmentName = "%sTo%s_ResM%d_M%dToInf_Interference_13TeV-pythia8_cff.py"%(model,decay,mass,massBins[i])
						outName = "%sTo%s_ResM%d_M%dToInf_Interference_13TeV-pythia8_forCRAB_cff.py"%(model,decay,mass,massBins[i])
					else:
						requestName = "%sTo%s_ResM%d_M%dTo%d_Interference_13TeV-pythia8"%(model,decay,mass,massBins[i],massBins[i+1])
						fragmentName = "%sTo%s_ResM%d_M%dTo%d_Interference_13TeV-pythia8_cff.py"%(model,decay,mass,massBins[i],massBins[i+1])
						outName = "%sTo%s_ResM%d_M%dTo%d_Interference_13TeV-pythia8_forCRAB_cff.py"%(model,decay,mass,massBins[i],massBins[i+1])
					with open('%s'%outName, "w") as outfile:
						subprocess.call(["python","runFragment.py","fragment=%s"%fragmentName,"decay=%s"%decayN],stdout=outfile)	

					crabCfg = crabTemplate%(requestName,outName,requestName,requestName)
					f = open("crabCfg.py","w")
					f.write(crabCfg)
					f.close()
					print fragmentName
					print requestName
					print outName
					print
					subprocess.call(["crab","submit","crabCfg.py"])
					exit()

	for mass in masses:
		for model in models:
			for decay, decayN in decays.iteritems():
				requestName = "%sTo%s_ResM%d_13TeV-pythia8"%(model,decay,mass)
				fragmentName = "%sTo%s_ResM%d_13TeV-pythia8_cff.py"%(model,decay,mass)
				outName = "%sTo%s_ResM%d_13TeV-pythia8_forCRAB_cff.py"%(model,decay,mass)
				with open('%s'%outName, "w") as outfile:
					subprocess.call(["python","runFragment.py","fragment=%s"%fragmentName,"decay=%s"%decayN],stdout=outfile)

				crabCfg = crabTemplate%(requestName,outName,requestName,requestName)
				f = open("crabCfg.py","w")
				f.write(crabCfg)
				f.close()
				subprocess.call(["crab","submit","crabCfg.py"])


model = "DY"
for i in range(0,len(massBins)-1):
	for decay, decayN in decays.iteritems():
		if massBins[i+1] == -1:
			requestName = "%sTo%s_M%dToInf_13TeV-pythia8"%(model,decay,massBins[i])
			fragmentName = "%sTo%s_M%dToInf_13TeV-pythia8_cff.py"%(model,decay,massBins[i])
			outName = "%sTo%s_M%dToInf_13TeV-pythia8_forCRAB_cff.py"%(model,decay,massBins[i])
		else:
			requestName = "%sTo%s_M%dTo%d_13TeV-pythia8"%(model,decay,massBins[i],massBins[i+1])
			fragmentName = "%sTo%s_M%dTo%d_13TeV-pythia8_cff.py"%(model,decay,massBins[i],massBins[i+1])
			outName = "%sTo%s_M%dTo%d_13TeV-pythia8_forCRAB_cff.py"%(model,decay,massBins[i],massBins[i+1])
		with open('%s'%outName, "w") as outfile:
				subprocess.call(["python","runFragment.py","fragment=%s"%fragmentName,"decay=%s"%decayN],stdout=outfile)	

		crabCfg = crabTemplate%(requestName,outName,requestName,requestName)
		f = open("crabCfg.py","w")
		f.write(crabCfg)
		f.close()
		subprocess.call(["crab","submit","crabCfg.py"])

