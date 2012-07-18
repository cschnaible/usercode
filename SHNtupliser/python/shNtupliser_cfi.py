import FWCore.ParameterSet.Config as cms

from SHarper.HEEPAnalyzer.HEEPEventParameters_cfi import *

shNtupliser = cms.EDAnalyzer("SHNtupliser", heepEventPara,
    outputFilename = cms.string("testOutput.root"),
    datasetCode = cms.int32(0),
    sampleWeight = cms.double(1.),
    minSCEtToPass = cms.double(15.),
    minNrSCToPass = cms.int32(-1),
    minJetEtToPass = cms.double(15.),
    minNrJetToPass = cms.int32(-1),                         
    addMet = cms.bool(True),
    addJets = cms.bool(True),
    addMuons = cms.bool(True),
    addTrigs = cms.bool(True),
    addCaloTowers =cms.bool(True),
    addCaloHits =cms.bool(True),
    addIsolTrks =cms.bool(True),
    addPFCands = cms.bool(False),
    writePDFInfo = cms.bool(False),
    fillFromGsfEle = cms.bool(True),
    minEtToPromoteSC = cms.double(-1.),
    outputGeom = cms.bool(True),                  
     # Isolation algos configuration
    intRadiusTk = cms.double(0.04), 
    ptMinTk = cms.double(0.0), 
    maxVtxDistTk = cms.double(0.2), 
    maxDrbTk = cms.double(0.1),
    etaSliceTk = cms.double(0.015),
    intRadiusHcal = cms.double(0.15),
    etMinHcal = cms.double(0.0), 
    intRadiusEcalBarrel = cms.double(3.0), 
    intRadiusEcalEndcaps = cms.double(3.0), 
    jurassicWidth = cms.double(1.5), 
    etMinBarrel = cms.double(0.0),
    eMinBarrel = cms.double(0.08), 
    etMinEndcaps = cms.double(0.1), 
    eMinEndcaps = cms.double(0.0),  
    vetoClustered  = cms.bool(False),  
    useNumCrystals = cms.bool(True),
    # debug para
    hltDebugFiltersToSave = cms.vstring(),
    useHLTDebug = cms.bool(False),
    hltIsoEleProducer = cms.InputTag("hltPixelMatchElectronsL1Iso"),
    hltNonIsoEleProducer = cms.InputTag("hltPixelMatchElectronsL1NonIso"),
    hltIsoEcalCandProducer = cms.InputTag("hltL1IsoRecoEcalCandidate"),
    hltNonIsoEcalCandProducer = cms.InputTag("hltL1NonIsoRecoEcalCandidate"),
    
    ecalProductsToSave = cms.vstring("clusShape:hltL1IsoHLTClusterShape:hltL1NonIsoHLTClusterShape",
                                     "hcalIsol:hltL1IsolatedElectronHcalIsol:hltL1NonIsolatedElectronHcalIsol"),
    eleProductsToSave = cms.vstring("dPhiIn:hltElectronL1IsoDetaDphi@Dphi:hltElectronL1NonIsoDetaDphi@Dphi",
                                    "dEtaIn:hltElectronL1IsoDetaDphi@Deta:hltElectronL1NonIsoDetaDphi@Deta"),                      
     
                             nrGenPartToStore = cms.int32(30),
                             compTwoMenus = cms.bool(False),
                             secondHLTTag = cms.string(""),
                             
                           
                             
    
) 


