import math

tune = 'cp5'


tuneInfo = {
        'cp5':{
            'tune_import':'from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *',
            'tune_settings_block':'pythia8CP5SettingsBlock',
            'tune_settings':'pythia8CP5Settings',
            'tune_pdf':'NNPDF31_nnlo_as_0118_mc',
            'tune_name':'NNPDF31nnlo_PR_TuneCP5',
            },
        'cp3':{ 
            'tune_import':'from Configuration.Generator.MCTunes2017.PythiaCP3Settings_cfi import *',
            'tune_settings_block':'pythia8CP3SettingsBlock',
            'tune_settings':'pythia8CP3Settings',
            'tune_pdf':'NNPDF31_nlo_as_0118',
            'tune_name':'NNPDF31nlo_TuneCP3',
            },
        }

template = '''
import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
%(tune_import)s
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
        comEnergy = cms.double(13000),
        filterEfficiency = cms.untracked.double(1),
        maxEventsToPrint = cms.untracked.int32(0),
        pythiaHepMCVerbosity = cms.untracked.bool(False),
        pythiaPylistVerbosity = cms.untracked.int32(1),
        PythiaParameters = cms.PSet(
	        pythia8CommonSettingsBlock,
            tune_settings_block,
            pythia8PSweightsSettingsBlock,
            processParameters = cms.vstring(
                        'NewGaugeBoson:ffbar2gmZZPrime = on',
                        'Zprime:gmZmode = %(interference)d',
                        'Zprime:universality = on',
                        'Zprime:vd=%(dV)f',
                        'Zprime:ad=%(dA)f',
                        'Zprime:vu=%(uV)f',
                        'Zprime:au=%(uA)f',
                        'Zprime:ve=%(eV)f',
                        'Zprime:ae=%(eA)f',
                        'Zprime:vnue=%(nuV)f',
                        'Zprime:anue=%(nuA)f',
                        '32:m0 = %(mass)d',
                        '32:onMode = off',
                        '32:onIfAny = %(decay)d',
                        'PhaseSpace:mHatMin = %(minMass)d',
                        'PhaseSpace:mHatMax = %(maxMass)d',
                        'PDF:pSet = LHAPDF6:%(tune_pdf)s',

            ),
        	parameterSets = cms.vstring('pythia8CommonSettings',
                                        '%(tune_settings)s',
                                        'pythia8PSweightsSettings',
        	                            'processParameters',
            )
	)
)
'''
#'PDF:pSet = LHAPDF6:%(PDFSET)s',

# Reference https://arxiv.org/abs/1010.6058 has numerical couplings 
# calculated using formulation similar to Halzen & Martin: gV, gA
# Using reference http://inspirehep.net/record/689807 to convert 
# to Pythia definitions of couplings: cV, cA
def cVcA_LR(VA):
    cosW = math.sqrt(1-0.2312)
    # cV = 2*cos(W)*gV*(gZp/gSU2)
    # cA = 2*cos(W)*gA*(gZp/gSU2)
    # gZp = 0.595, gSU2 = 0.652
    gLR,gSU2 = 0.595, 0.652
    return 2*cosW*VA*(gLR/gSU2)

def cVcA_SM(VA):
    # cV = 2*gV
    # cA = 2*gA
    # simplifies from gZp = gSU2/cosW
    return 2*VA


def setZPrimeParams(model):
	result = {}
	if model=='ZprimeChi':
	    print "Z' chi "
	    sinThetaW=math.sqrt(0.23)
	    result["dV"]=2*math.sqrt(6)*sinThetaW/3
	    result["dA"]=-math.sqrt(6)*sinThetaW/3
	    result["uV"]=0
	    result["uA"]=math.sqrt(6)*sinThetaW/3
	    result["eV"]=-result["dV"]
	    result["eA"]=result["dA"]
	    result["nuV"]=-math.sqrt(6)*sinThetaW/2;
	    result["nuA"]=result["nuV"]

	    
	elif model=="ZprimeEta":
	    print "Z' eta"
	    sinThetaW=math.sqrt(0.23)
	    result["dV"]=sinThetaW
	    result["dA"]=sinThetaW/3
	    result["uV"]=0
	    result["uA"]=4*sinThetaW/3
	    result["eV"]=-result["dV"]
	    result["eA"]=result["dA"]
	    result["nuV"]=-sinThetaW/3;
	    result["nuA"]=result["nuV"]

	elif model=="ZprimeI":
	    print "Z' I"
	    sinThetaW=math.sqrt(0.23)
	    
	    result["dV"]=math.sqrt(15)/3*sinThetaW
	    result["dA"]=-math.sqrt(15)/3*sinThetaW
	    result["uV"]=0
	    result["uA"]=0
	    result["eV"]=-result["dV"]
	    result["eA"]=result["dA"]
	    result["nuV"]=result["eV"]
	    result["nuA"]=result["eA"]
	    
	elif model=="ZprimeSQ":
	    print "Z' SQ"
	    sinThetaW=math.sqrt(0.23)
	    
	    result["dV"]=3/2*sinThetaW
	    result["dA"]=-7/6*sinThetaW
	    result["uV"]=0
	    result["uA"]=sinThetaW/3
	    result["eV"]=-result["dV"]
	    result["eA"]=result["dA"]
	    result["nuV"]=-4/3*sinThetaW
	    result["nuA"]=-4/3*sinThetaW
	elif model=="ZprimeN":
	    print "Z' N"
	    sinThetaW=math.sqrt(0.23)
	    
	    result["dV"]=-math.sqrt(6)/6*sinThetaW
	    result["dA"]=math.sqrt(6)/2*sinThetaW
	    result["uV"]=0
	    result["uA"]=math.sqrt(6)/3*sinThetaW
	    result["eV"]=-result["dV"]
	    result["eA"]=result["dA"]
	    result["nuV"]=math.sqrt(6)/3*sinThetaW
	    result["nuA"]=math.sqrt(6)/3*sinThetaW

	elif model=="ZprimePSI":
	    print "Z' PSI"
	    result["dV"]=0
	    result["dA"]=0.506809
	    result["uV"]=0
	    result["uA"]=0.506809
	    result["eV"]=0
	    result["eA"]=0.506809
	    result["nuV"]=0.253405
	    result["nuA"]=0.253405

	elif model=="ZprimeSSM" or model=="DY":
	    print "Z' SSM or DY"
	    result["dV"] = -0.693
	    result["dA"] = -1.
	    result["uV"] = 0.387
	    result["uA"] = 1.
	    result["eV"] = -0.08
	    result["eA"] = -1.
	    result["nuV"] = 1
	    result["nuA"] = 1
	 
	elif model=="ZprimeQ":
	    print "Z' Q"
	    result["dV"] = -1.333
	    result["dA"] = 0.
	    result["uV"] = 2.666
	    result["uA"] = 0.
	    result["eV"] = -4.0
	    result["eA"] = 0
	    result["nuV"] = 0
	    result["nuA"] = 0
	elif model=="ZprimeT3L":
	    print "Z' T3L"
	    result["dV"] = cVcA_SM(-0.5)
	    result["dA"] = cVcA_SM(-0.5)
	    result["uV"] = cVcA_SM(0.5)
	    result["uA"] = cVcA_SM(0.5)
	    result["eV"] = cVcA_SM(-0.5)
	    result["eA"] = cVcA_SM(-0.5)
	    result["nuV"] = cVcA_SM(0.5)
	    result["nuA"] = cVcA_SM(0.5)
	
	elif model=="ZprimeR":
	    print "Z' R"
	    result["dV"] = cVcA_LR(-0.5)
	    result["dA"] = cVcA_LR(0.5)
	    result["uV"] =  cVcA_LR(0.5)
	    result["uA"] =  cVcA_LR(-0.5)
	    result["eV"] =  cVcA_LR(-0.5)
	    result["eA"] =  cVcA_LR(0.5)
	    result["nuV"] =  cVcA_LR(0.)
	    result["nuA"] =  cVcA_LR(0.)

	elif model=="ZprimeLR":
	    print "Z' LR"
	    result["dV"] = cVcA_LR(-0.591)
	    result["dA"] = cVcA_LR(0.46)
	    result["uV"] = cVcA_LR(0.329)
	    result["uA"] = cVcA_LR(-0.46)
	    result["eV"] = cVcA_LR(0.068)
	    result["eA"] = cVcA_LR(0.46)
	    result["nuV"] = cVcA_LR(0.196)
	    result["nuA"] = cVcA_LR(0.196)

	elif model=="ZprimeY":
	    print "Z' Y"
	    result["dV"] = cVcA_LR(-0.167)
	    result["dA"] = cVcA_LR(0.5)
	    result["uV"] = cVcA_LR(0.833)
	    result["uA"] = cVcA_LR(-0.5)
	    result["eV"] = cVcA_LR(-1.5)
	    result["eA"] = cVcA_LR(0.5)
	    result["nuV"] = cVcA_LR(-0.5) 
	    result["nuA"] =  cVcA_LR(-0.5)
	    
	elif model=="ZprimeB-L":
	    print "Z' B-L"
	    result["dV"] = cVcA_LR(0.333)
	    result["dA"] = cVcA_LR(0.)
	    result["uV"] = cVcA_LR(0.333)
	    result["uA"] = cVcA_LR(0.)
	    result["eV"] = cVcA_LR(-1.)
	    result["eA"] = cVcA_LR(0.)
	    result["nuV"] = cVcA_LR(-0.5)
	    result["nuA"] = cVcA_LR(-0.5)
	    
	return result
PDFSETS = {
        'NNPDF30NLO':'NNPDF30_nlo_as_0118',
        'NNPDF31NLO':'NNPDF31_nlo_as_0118',
        'PDF4LHC15NLOMC':'PDF4LHC15_nlo_mc',
        'CT10NLO':'CT10nlo',
        'CT14NLO':'CT14nlo',
        }

# option 0 : full gamma^*/Z^0/Z'^0 structure, with interference included. 
# option 1 : only pure gamma^* contribution. 
# option 2 : only pure Z^0 contribution. 
# option 3 : only pure Z'^0 contribution. 
# option 4 : only the gamma^*/Z^0 contribution, including interference. 
# option 5 : only the gamma^*/Z'^0 contribution, including interference. 
# option 6 : only the Z^0/Z'^0 contribution, including interference. 
interference = 0 # turns on interference, set to 3 for Z' only and 4 for Z/gamma Drell-Yan

masses = [9000]#[6000,9000,12000]
massBins = [120,200,400,800,1400,2300,3500,4500,6000,-1]
#models = ['ZprimeQ','ZprimeSSM','ZprimePSI','ZprimeN','ZprimeSQ','ZprimeI','ZprimeEta','ZprimeChi','DY','ZprimeR','ZprimeB-L','ZprimeLR','ZprimeY','ZprimeT3L']
models = ['DY','ZprimeQ']
#decays = {'EE':11,'MuMu':13}
decays = {'MuMu':13}
savedir = 'fragments_nnpdf31'

# Zprime+DY interference and DY-only fragments
for tune in tuneInfo:
    pdftouse = tuneInfo[tune]['tune_name']
    for mass in masses:
        for i in range(0,len(massBins)-1):
            for model in models:
                for decay, decayN in decays.iteritems():
                    print model,decayN,mass
                    params = setZPrimeParams(model)
                    params["mass"] = mass
                    params["minMass"] = massBins[i]
                    params["maxMass"] = massBins[i+1]
                    params["decay"] = decayN
                    params["interference"] = interference
                    for info in tuneInfo[tune].keys():
                        params[info] = tuneInfo[tune][info]
                    #params["PDFSET"] = PDFSETS[pdftouse]
                    if model == "DY":
                        params["interference"] = 4
                    #print params
                    fragment = template%params
                    if model == "DY":
                        if massBins[i+1] == -1:
                            f = open(savedir+"/%sTo%s_M-%dToInf_%s_13TeV-pythia8_cff.py"%(model,decay,massBins[i],pdftouse),"w")
                        else:
                            f = open(savedir+"/%sTo%s_M-%dTo%d_%s_13TeV-pythia8_cff.py"%(model,decay,massBins[i],massBins[i+1],pdftouse),"w")
                    else:
                        if massBins[i+1] == -1:
                            f = open(savedir+"/%sTo%s_M%d_M-%dToInf_%s_Interference_13TeV-pythia8_cff.py"%(model,decay,mass,massBins[i],pdftouse),"w")
                        else:
                            f = open(savedir+"/%sTo%s_M%d_M-%dTo%d_%s_Interference_13TeV-pythia8_cff.py"%(model,decay,mass,massBins[i],massBins[i+1],pdftouse),"w")
                    f.write(fragment)
                    f.close()

# Zprime only fragments
for tune in tuneInfo:
    pdftouse = tuneInfo[tune]['tune_name']
    interference = 3 # turns on interference, set to 3 for Z' only and 4 for Z/gamma Drell-Yan
    for mass in masses:
        for model in models:
            for decay, decayN in decays.iteritems():
                if model == "DY": continue
                params = setZPrimeParams(model)
                params["mass"] = mass
                params["minMass"] = -1
                params["maxMass"] = -1
                params["decay"] = decayN
                params["interference"] = interference
                #params["PDFSET"] = PDFSETS[pdftouse]
                for info in tuneInfo[tune].keys():
                    params[info] = tuneInfo[tune][info]
                fragment = template%params
                f = open(savedir+"/%sTo%s_M%d_%s_13TeV-pythia8_cff.py"%(model,decay,mass,pdftouse),"w")
                f.write(fragment)
                f.close()
