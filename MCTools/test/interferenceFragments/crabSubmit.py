import subprocess

crabTemplate='''
from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = '%s'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True


config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = '%s'

config.section_("Data")
config.Data.outputPrimaryDataset = '%s'
config.Data.inputDBS = 'global'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 100000
config.Data.totalUnits = 100000
config.Data.publication = False
config.Data.publishDBS = 'phys03' 
config.Data.outputDatasetTag = '%s'
config.Data.outLFNDirBase = '/store/user/jschulte/'
 
config.section_("Site")
config.Site.storageSite = "T2_US_Purdue"

config.section_("User")
'''


interference = 0 # turns on interference, set to 3 for Z' only and 4 for Z/gamma Drell-Yan
#masses = [1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000]
masses = [4000,6000]
massBins = [120,200,400,800,1400,2300,3500,4500,6000,-1]
#models = ["ZPrimeQ","ZPrimeSSM","ZPrimePSI","ZPrimeN","ZPrimeSQ","ZPrimeI","ZPrimeEta","ZPrimeChi"]
models = ["ZPrimeQ","ZPrimeSSM","ZPrimePSI","ZPrimeN","ZPrimeSQ","ZPrimeI","ZPrimeEta","ZPrimeChi"]
decays = {"EE":11}
#decays = {"EE":11,"MuMu":13}
if False:
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
						subprocess.call(["python","runFragment.py","fragment=%s"%fragmentName],stdout=outfile)	

					crabCfg = crabTemplate%(requestName,outName,requestName,requestName)
					f = open("crabCfg.py","w")
					f.write(crabCfg)
					f.close()
					subprocess.call(["crab","submit","crabCfg.py"])

	for mass in masses:
		for model in models:
			for decay, decayN in decays.iteritems():
				requestName = "%sTo%s_ResM%d_13TeV-pythia8"%(model,decay,mass)
				fragmentName = "%sTo%s_ResM%d_13TeV-pythia8_cff.py"%(model,decay,mass)
				outName = "%sTo%s_ResM%d_13TeV-pythia8_forCRAB_cff.py"%(model,decay,mass)
				with open('%s'%outName, "w") as outfile:
					subprocess.call(["python","runFragment.py","fragment=%s"%fragmentName],stdout=outfile)	

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
			subprocess.call(["python","runFragment.py","fragment=%s"%fragmentName],stdout=outfile)	

		crabCfg = crabTemplate%(requestName,outName,requestName,requestName)
		f = open("crabCfg.py","w")
		f.write(crabCfg)
		f.close()
		subprocess.call(["crab","submit","crabCfg.py"])

