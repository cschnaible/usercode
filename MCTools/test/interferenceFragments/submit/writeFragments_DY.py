import math

template = '''
import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
        comEnergy = cms.double(13000),
        filterEfficiency = cms.untracked.double(1),
        maxEventsToPrint = cms.untracked.int32(0),
        pythiaHepMCVerbosity = cms.untracked.bool(False),
        pythiaPylistVerbosity = cms.untracked.int32(1),
        PythiaParameters = cms.PSet(
	        pythia8CommonSettingsBlock,
            pythia8CUEP8M1SettingsBlock,
            processParameters = cms.vstring(
                        'WeakSingleBoson:ffbar2gmZ = on',
                        '23:onMode = off',
                        '23:onIfAny = %(decay)d',
                        'PhaseSpace:mHatMin = %(minMass)d',
                        'PhaseSpace:mHatMax = %(maxMass)d',
                        'PDF:pSet = LHAPDF6:%(PDFSET)s',

            ),
        	parameterSets = cms.vstring('pythia8CommonSettings',
	                                    'pythia8CUEP8M1Settings',
        	                            'processParameters',
            )
	)
)
'''

PDFSETS = {
        'NNPDF30nlo':'NNPDF30_nlo_as_0118',
        'NNPDF31nlo':'NNPDF31_nlo_as_0118',
        'PDF4LHC15nlomc':'PDF4LHC15_nlo_mc',
        'CT10nlo':'CT10nlo',
        'CT14nlo':'CT14nlo',
        }

massBinsLow =  ['120','200','400','800','1400','2300','3500','4500','6000']
massBinsHigh = ['200','400','800','1400','2300','3500','4500','6000','Inf']
massBins = {
        '120':120,
        '200':200,
        '400':400,
        '800':800,
        '1400':1400,
        '2300':2300,
        '3500':3500,
        '4500':4500,
        '6000':6000,
        'Inf':-1,
        }

#decays = {"EE":11,"MuMu":13}
decays = {"EE":11}
#decays = {"MuMu":13}

#pdfs = ['CT10nlo','CT14nlo']#,'MMHT2014nlo68cl']
pdfs = ['NNPDF30nlo']#,'MMHT2014nlo68cl']

# DY-only fragments
params = {}
for pdftouse in pdfs:
    for low,high in zip(massBinsLow,massBinsHigh):
        for decay, decayN in decays.iteritems():
            params["minMass"] = massBins[low]
            params["maxMass"] = massBins[high]
            params["decay"] = decayN
            params["PDFSET"] = PDFSETS[pdftouse]
            fragment = template%params
            f = open("DYTo%s_M%sTo%s_13TeV-pythia8_%s_cff.py"%(decay,low,high,pdftouse),"w")
            f.write(fragment)
            f.close()
