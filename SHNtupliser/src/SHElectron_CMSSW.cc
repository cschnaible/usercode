#include "SHarper/SHNtupliser/interface/SHElectron.hh"

#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"

#include "SHarper/HEEPAnalyzer/interface/HEEPEle.h"


//removed
SHElectron::SHElectron(const heep::Ele& ele,int superClusNr)
{
  

}

//fills off a GsfElectron, doesnt fill nr trks isol or cutcode
SHElectron::SHElectron(const reco::GsfElectron& ele,int superClusNr):
  //classification variables
type_(ele.classification()),
//kinematic quantities
p4_(ele.px()/ele.energy()*ele.ecalEnergy(),ele.py()/ele.energy()*ele.ecalEnergy(),ele.pz()/ele.energy()*ele.ecalEnergy(),ele.ecalEnergy()),
et_(p4_.Pt()),
nrgy_(ele.ecalEnergy()),
rawNrgy_(ele.superCluster()->rawEnergy()),
preShowerNrgy_(ele.superCluster()->preshowerEnergy()),
nrgyErr_(ele.ecalEnergyError()),
posCal_(ele.caloPosition().X(),ele.caloPosition().Y(),ele.caloPosition().Z()),
e5x5_(ele.full5x5_e5x5()),
eta_(ele.eta()),
detEta_(ele.superCluster()->eta()),
//track quantities (momentum + positions)
//momemtums
p3TrackVtx_(ele.trackMomentumAtVtx().X(),ele.trackMomentumAtVtx().Y(),ele.trackMomentumAtVtx().Z()),
p3TrackCal_(ele.trackMomentumAtCalo().X(),ele.trackMomentumAtCalo().Y(),ele.trackMomentumAtCalo().Z()),
//p3TrackInn_(ele.gsfTrack()->innerMomentum().X(),ele.gsfTrack()->innerMomentum().Y(),ele.gsfTrack()->innerMomentum().Z()),
p3TrackInn_(ele.gsfTrack()->px(),ele.gsfTrack()->py(),ele.gsfTrack()->pz()),
p3TrackOut_(ele.trackMomentumOut().X(),ele.trackMomentumOut().Y(),ele.trackMomentumOut().Z()),
//positions
posTrackVtx_(ele.TrackPositionAtVtx().X(),ele.TrackPositionAtVtx().Y(),ele.TrackPositionAtVtx().Z()),
posTrackCal_(ele.TrackPositionAtCalo().X(),ele.TrackPositionAtCalo().Y(),ele.TrackPositionAtCalo().Z()),
posTrackInn_(ele.gsfTrack()->vx(),ele.gsfTrack()->vy(),ele.gsfTrack()->vz()),
//posTrackInn_(ele.gsfTrack()->innerPosition().X(),ele.gsfTrack()->innerPosition().Y(),ele.gsfTrack()->innerPosition().Z()),
//posTrackOut_(ele.gsfTrack()->outerPosition().X(),ele.gsfTrack()->outerPosition().Y(),ele.gsfTrack()->outerPosition().Z()),
//posTrackInn_(0.001,0,0.),
posTrackOut_(0.001,0,0.),
trkChi2_(ele.gsfTrack()->chi2()),
nrDof_(static_cast<int>(ele.gsfTrack()->ndof())),
posCharge_(ele.charge()>0),
d0_(999),
//id quantities
epIn_(ele.eSuperClusterOverP()),
epOut_(ele.eSeedClusterOverPout()),
hadem_(ele.hcalOverEcal()),
hademDepth1_(ele.hcalDepth1OverEcal()), 
hademDepth2_(ele.hcalDepth2OverEcal()),
dEtaIn_(ele.deltaEtaSuperClusterTrackAtVtx()),
dEtaOut_(ele.deltaEtaSeedClusterTrackAtCalo()),
dPhiIn_(ele.deltaPhiSuperClusterTrackAtVtx()),
dPhiOut_(ele.deltaPhiSeedClusterTrackAtCalo()),
sigmaEtaEta_(ele.full5x5_sigmaEtaEta()),
sigmaIEtaIEta_(ele.full5x5_sigmaIetaIeta()),
sigmaIPhiIPhi_(ele.full5x5_sigmaIphiIphi()),
//links to tracks, superClusters
superClusIndx_(superClusNr),
isolEm_(ele.dr03EcalRecHitSumEt()),
isolHad_(ele.dr03HcalTowerSumEt()),
isolHadDepth1_(ele.dr03HcalDepth1TowerSumEt()),
isolHadDepth2_(ele.dr03HcalDepth2TowerSumEt()),
isolPtTrks_(ele.dr03TkSumPt()),
isolNrTrks_(-1), //not really supported anymore
cutCode_(-1),
e1x5Over5x5_(ele.full5x5_e1x5()/ele.full5x5_e5x5()),
e2x5Over5x5_(ele.full5x5_e2x5Max()/ele.full5x5_e5x5()),
isEcalDriven_(ele.ecalDrivenSeed()),
isTrackerDriven_(ele.trackerDrivenSeed()),
isolEmDR04_(ele.dr04EcalRecHitSumEt()),
isolHadDepth1DR04_(ele.dr04HcalDepth1TowerSumEt()),
isolHadDepth2DR04_(ele.dr04HcalDepth2TowerSumEt()),
isolPtTrksDR04_(ele.dr04TkSumPt()),
epCombNrgy_(ele.energy()),
seedId_(ele.superCluster()->seed()->seed().rawId()),
isBarrel_(ele.isEB()),
isEBEEGap_(ele.isEBEEGap()), 
isEBEtaGap_(ele.isEBEtaGap()),  
isEBPhiGap_(ele.isEBPhiGap()), 
isEEDeeGap_(ele.isEEDeeGap()),  
isEERingGap_(ele.isEERingGap()),
posChargeTrk_(ele.gsfTrack()->charge()),
nrMissingHits_(ele.gsfTrack()->hitPattern().numberOfHits(reco::HitPattern::MISSING_INNER_HITS)),
//nrMissingHits_(-1),
dCotTheta_(ele.convDcot()),
dist_(ele.convDist()),
radius_(ele.convRadius()),
isolChargedHadron_(ele.pfIsolationVariables().sumChargedHadronPt),
isolNeutralHadron_(ele.pfIsolationVariables().sumNeutralHadronEt),
isolPhoton_(ele.pfIsolationVariables().sumPhotonEt),
hademDepth1BC_(ele.hcalDepth1OverEcalBc()),
hademDepth2BC_(ele.hcalDepth2OverEcalBc()),
isolHadDepth1BC_(ele.dr03HcalDepth1TowerSumEtBc()),
isolHadDepth2BC_(ele.dr03HcalDepth2TowerSumEtBc()),
dxyErr_(ele.gsfTrack()->dxyError()),
dzErr_(ele.gsfTrack()->dzError()),
isolMVA_(ele.mvaOutput().mva_Isolated),
nonIsolMVA_(ele.mvaOutput().mva_e_pi),
passCutPreSel_(ele.passingCutBasedPreselection()),
passMVAPreSel_(ele.passingMvaPreselection()),
passPFlowPreSel_(ele.passingPflowPreselection()),  
pmDPhi1_(ele.pixelMatchDPhi1()),
pmDPhi2_(ele.pixelMatchDPhi1()),
pmDRz1_(ele.pixelMatchDPhi1()),
pmDRz2_(ele.pixelMatchDPhi1()),
pmSubDets_(ele.pixelMatchSubdetector1()*10+ele.pixelMatchSubdetector2()),
rhoCorr_(-999.),
mEvent_(NULL)
{
 
 

}
//fills off a GsfElectron, doesnt fill nr trks isol or cutcode
SHElectron::SHElectron(const reco::Photon& pho,int superClusNr):
  //classification variables
type_(0),
//kinematic quantities
p4_(pho.px(),pho.py(),pho.pz(),pho.energy()),
et_(p4_.Pt()),
nrgy_(pho.energy()),
rawNrgy_(pho.superCluster()->rawEnergy()),
preShowerNrgy_(pho.superCluster()->preshowerEnergy()),
nrgyErr_(-1),
posCal_(pho.caloPosition().X(),pho.caloPosition().Y(),pho.caloPosition().Z()),
e5x5_(pho.full5x5_e5x5()),
eta_(pho.eta()),
detEta_(pho.superCluster()->eta()),

//track quantities (momentum + positions)
//momemtums
p3TrackVtx_(0.001,0,0.),
p3TrackCal_(0.001,0,0.),
p3TrackInn_(0.001,0,0.),
p3TrackOut_(0.001,0,0.),
//positions
posTrackVtx_(0.001,0,0.),
posTrackCal_(0.001,0,0.),
posTrackInn_(0.001,0,0.),
posTrackOut_(0.001,0,0.),
trkChi2_(-1),
nrDof_(-1),
posCharge_(0),
d0_(999),
//id quantities
epIn_(-1),
epOut_(-1),
hadem_(pho.hadronicOverEm()),
hademDepth1_(pho.hadronicDepth1OverEm()), 
hademDepth2_(pho.hadronicDepth2OverEm()),
dEtaIn_(999.),
dEtaOut_(999.),
dPhiIn_(999.),
dPhiOut_(999.),
sigmaEtaEta_(pho.full5x5_sigmaEtaEta()),
sigmaIEtaIEta_(pho.full5x5_sigmaIetaIeta()),
sigmaIPhiIPhi_(999.),
//links to tracks, superClusters
superClusIndx_(superClusNr),
isolEm_(pho.ecalRecHitSumEtConeDR03()),
isolHad_(pho.hcalTowerSumEtConeDR03()),
isolHadDepth1_(pho.hcalDepth1TowerSumEtConeDR03()),
isolHadDepth2_(pho.hcalDepth2TowerSumEtConeDR03()),
isolPtTrks_(pho.trkSumPtHollowConeDR03()),
isolNrTrks_(-1), //not really supported anymore
cutCode_(-1),
e1x5Over5x5_(pho.full5x5_e1x5()/pho.full5x5_e5x5()),
e2x5Over5x5_(pho.full5x5_e2x5()/pho.full5x5_e5x5()),
isEcalDriven_(1),
isTrackerDriven_(0),
isolEmDR04_(pho.ecalRecHitSumEtConeDR04()),
isolHadDepth1DR04_(pho.hcalDepth1TowerSumEtConeDR04()),
isolHadDepth2DR04_(pho.hcalDepth2TowerSumEtConeDR04()),
isolPtTrksDR04_(pho.trkSumPtHollowConeDR04()),
epCombNrgy_(pho.energy()),
seedId_(pho.superCluster()->seed()->seed().rawId()),
isBarrel_(pho.isEB()),
isEBEEGap_(pho.isEBEEGap()), 
isEBEtaGap_(pho.isEBEtaGap()),  
isEBPhiGap_(pho.isEBPhiGap()), 
isEEDeeGap_(pho.isEEDeeGap()),  
isEERingGap_(pho.isEERingGap()),
posChargeTrk_(0),
nrMissingHits_(-1),
dCotTheta_(-1),
dist_(-1),
radius_(-999),
isolChargedHadron_(pho.chargedHadronIso()),
isolNeutralHadron_(pho.neutralHadronIso()),
isolPhoton_(pho.photonIso()),
hademDepth1BC_(pho.hadTowDepth1OverEm()),
hademDepth2BC_(pho.hadTowDepth2OverEm()),
isolHadDepth1BC_(-999.),
isolHadDepth2BC_(-999.),
dxyErr_(-999.),
dzErr_(-999.),
isolMVA_(-999.),
nonIsolMVA_(-999.),  
passCutPreSel_(false),
passMVAPreSel_(false),
passPFlowPreSel_(false),  
pmDPhi1_(-999.),
pmDPhi2_(-999.),
pmDRz1_(-999.),
pmDRz2_(-999.),
pmSubDets_(0),
rhoCorr_(-999.),
mEvent_(NULL)
{
 
 

}


//makes a trackless electron
SHElectron::SHElectron(const TLorentzVector&p4,const reco::SuperCluster& superClus,
		       const cmssw::FiducialFlags& fid,
		       const cmssw::ShowerShape& shape,
		       const cmssw::IsolationVariables& isol03,
		       const cmssw::IsolationVariables& isol04,
		       int superClusNr):
//classification variables
  type_(0), //all are golden (dump this variable...)
  //kinematic quantities
  p4_(p4),
  et_(p4_.Pt()),
  nrgy_(p4_.E()),
  rawNrgy_(superClus.rawEnergy()),
  preShowerNrgy_(superClus.preshowerEnergy()),
  nrgyErr_(-999), //too complicated to fill for now
  posCal_(superClus.x(),superClus.y(),superClus.z()),
  e5x5_(shape.e5x5),
  eta_(p4.Eta()),
  detEta_(superClus.eta()),
  //track quantities (momentum + positions)
  //momemtums
  p3TrackVtx_(0.001,0,0.),
  p3TrackCal_(0.001,0,0.),
  p3TrackInn_(0.001,0,0.),
  p3TrackOut_(0.001,0,0.),
  //positions
  posTrackVtx_(0.001,0,0.),
  posTrackCal_(0.001,0,0.),
  posTrackInn_(0.001,0,0.),
  posTrackOut_(0.001,0,0.),
  trkChi2_(999999),
  nrDof_(static_cast<int>(1)),
  posCharge_(0),
  d0_(999),
  //id quantities
  epIn_(999999),
  epOut_(999999),
  hadem_(shape.hcalDepth1OverEcal+shape.hcalDepth2OverEcal),
  hademDepth1_(shape.hcalDepth1OverEcal), 
  hademDepth2_(shape.hcalDepth2OverEcal),
  dEtaIn_(999),
  dEtaOut_(999),
  dPhiIn_(999),
  dPhiOut_(999),
  sigmaEtaEta_(shape.sigmaEtaEta),
  sigmaIEtaIEta_(shape.sigmaIetaIeta),
  sigmaIPhiIPhi_(999),
  //links to tracks, superClusters
  superClusIndx_(superClusNr),
  isolEm_(isol03.ecalRecHitSumEt),
  isolHad_(isol03.hcalDepth1TowerSumEt+isol03.hcalDepth2TowerSumEt),
  isolHadDepth1_(isol03.hcalDepth1TowerSumEt),
  isolHadDepth2_(isol03.hcalDepth2TowerSumEt),
  isolPtTrks_(isol03.tkSumPt),
  isolNrTrks_(-1), //not really supported anymore
  cutCode_(-1),
  e1x5Over5x5_(shape.e1x5/shape.e5x5),
  e2x5Over5x5_(shape.e2x5Max/shape.e5x5),
  isEcalDriven_(1),
  isTrackerDriven_(0),
  isolEmDR04_(isol04.ecalRecHitSumEt),
  isolHadDepth1DR04_(isol04.hcalDepth1TowerSumEt),
  isolHadDepth2DR04_(isol04.hcalDepth2TowerSumEt),
  isolPtTrksDR04_(isol04.tkSumPt),
  epCombNrgy_(-999),
  seedId_(superClus.seed()->seed().rawId()),
  isBarrel_(fid.isEB),
  isEBEEGap_(fid.isEBEEGap), 
  isEBEtaGap_(fid.isEBEtaGap),  
  isEBPhiGap_(fid.isEBPhiGap), 
  isEEDeeGap_(fid.isEEDeeGap),  
  isEERingGap_(fid.isEERingGap),
  posChargeTrk_(0),
  nrMissingHits_(-1),
  dCotTheta_(-1),
  dist_(-1),
  radius_(-999),
  isolChargedHadron_(-999.),
  isolNeutralHadron_(-999.),
  isolPhoton_(-999.),
  hademDepth1BC_(-999.),
  hademDepth2BC_(-999.),
  isolHadDepth1BC_(-999.),
  isolHadDepth2BC_(-999.),
  dxyErr_(-999.),
  dzErr_(-999.),
  passCutPreSel_(false),
  passMVAPreSel_(false),
  passPFlowPreSel_(false),  
  pmDPhi1_(-999.),
  pmDPhi2_(-999.),
  pmDRz1_(-999.),
  pmDRz2_(-999.),
  pmSubDets_(0),
  rhoCorr_(-999.),
  mEvent_(NULL)
{
}


