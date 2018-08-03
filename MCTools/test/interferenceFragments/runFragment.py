
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('analysis')
from SHarper.MCTools.mcCmdLineOptions_cfi import registerDefaultMCOptions
registerDefaultMCOptions(options)
options.register ('fragment',
                  "ZPrimeSSMToMuMu_ResM7000_M800To1400_Interference_13TeV-pythia8_cff.py",
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.string,
                  "which generator fragment to run")
options.parseArguments()


import FWCore.ParameterSet.Config as cms


process = cms.Process('GEN')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedNominalCollision2015_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
    reportEvery = cms.untracked.int32(500),
    limit = cms.untracked.int32(10000000)
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)
# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_71_V1::All')

process.load(options.fragment.split(".")[0])

process.ProductionFilterSequence = cms.Sequence(process.generator)
datasetCode=10001
if "ResM" in options.fragment:
	massVal = float(options.fragment.split("_")[1].split("ResM")[-1])
else:
	massVal = 91.2
process.crossSecTreeMaker =  cms.EDAnalyzer("CrossSecTreeMaker",
                                            mass=cms.double(massVal),
                                            datasetName=cms.string(options.fragment.split(".")[0]+".root"),
                                            datasetCode=cms.int32(datasetCode),
                                            cmsEnergy=cms.double(13)
                                            )

process.pdfTreeMaker = cms.EDAnalyzer("PDFTreeMaker",
                                      datasetCode=cms.int32(datasetCode),
                                      genPartsTag=cms.InputTag("genParticles"),
                                      decayParticlePID = cms.int32(11),
                                      genEvtInfoTag = cms.InputTag("generator"),
                                      pdfWeightsTag=cms.InputTag("dummy"),
                                     #  pdfWeightsTag=cms.InputTag("pdfWeights:MRST2006nnlo")
                                      )


process.pdfWeights = cms.EDProducer("PdfWeightProducer",
                                    # Fix POWHEG if buggy (this PDF set will also appear on output,
                                    # so only two more PDF sets can be added in PdfSetNames if not "")
                                    #FixPOWHEG = cms.untracked.string("cteq66.LHgrid"),
                                    #GenTag = cms.untracked.InputTag("genParticles"),
                                    PdfInfoTag = cms.untracked.InputTag("generator"),
                                    PdfSetNames = cms.untracked.vstring(
                                        "cteq66.LHgrid",
                                    #  "MRST2006nnlo.LHgrid",
                                    #   "NNPDF10_100.LHgrid"
                                        )
      )

    

if options.cmsswOutput:
    process.outputTot = cms.OutputModule( "PoolOutputModule",
                                          fileName = cms.untracked.string(options.fragment.split(".")[0]+".root" ),
                                          fastCloning = cms.untracked.bool( False ),
                                          dataset = cms.untracked.PSet(
                                              filterName = cms.untracked.string( "" ),
                                              dataTier = cms.untracked.string( "RAW" )
                                              ),
                                             
                                          outputCommands = cms.untracked.vstring( 'drop *','keep recoGenParticles_genParticles_*_*')                                             )
    outputMod = process.outputTot
else:
    
    process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string(options.fragment.split(".")[0]+".root")
                                       )
    outputMod = process.TFileService

isCrabJob=False #script seds this if its a crab job
#if 1, its a crab job...
if isCrabJob:
    print "using crab specified filename"
    outputMod.fileName= "OUTPUTFILE"    

# Path and EndPath definitions
if options.cmsswOutput:
    process.generation_step = cms.Path(process.pgen)
    process.endjob_step = cms.EndPath(process.endOfProcess*process.outputTot)
else:
    process.generation_step = cms.Path(process.pgen*process.crossSecTreeMaker*process.pdfTreeMaker)
    process.endjob_step = cms.EndPath(process.endOfProcess)

process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 

print process.dumpPython()
