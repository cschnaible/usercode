#include "SHarper/SHNtupliser/interface/SHNtupliser.h"

#include "SHarper/SHNtupliser/interface/SHEvent.hh"
#include "SHarper/SHNtupliser/interface/SHCaloGeom.hh"
#include "SHarper/SHNtupliser/interface/GeomFuncs.hh"
#include "SHarper/SHNtupliser/interface/SHGeomFiller.h"
#include "SHarper/SHNtupliser/interface/TrigDebugObjHelper.h"
#include "SHarper/SHNtupliser/interface/SHTrigObjContainer.hh"
#include "SHarper/SHNtupliser/interface/SHPFCandContainer.hh"
#include "SHarper/SHNtupliser/interface/SHTrigSumMaker.h"
#include "SHarper/SHNtupliser/interface/PFFuncs.h"
#include "SHarper/SHNtupliser/interface/GenFuncs.h"

#include "SHarper/HEEPAnalyzer/interface/HEEPDebug.h"


#include "DataFormats/EgammaReco/interface/SuperClusterFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"
#include "DataFormats/L1Trigger/interface/L1EmParticle.h"

#include "CondFormats/L1TObjects/interface/L1GtTriggerMenu.h"
#include "CondFormats/DataRecord/interface/L1GtTriggerMenuRcd.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutSetupFwd.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutSetup.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"

#include "RecoEgamma/EgammaIsolationAlgos/interface/EgammaTowerIsolation.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterTools.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "TFile.h"
#include "TTree.h"

#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
void filterHcalHits(const SHEvent* event,double maxDR,const SHCaloHitContainer& inputHits,SHCaloHitContainer& outputHits);
void filterEcalHits(const SHEvent* event,double maxDR,const SHCaloHitContainer& inputHits,SHCaloHitContainer& outputHits);
void filterCaloTowers(const SHEvent* event,double maxDR,const SHCaloTowerContainer& inputHits,SHCaloTowerContainer& outputHits);

void fillPFClustersECAL(const SHEvent* event,double maxDR,SHPFClusterContainer& shPFClusters,const std::vector<reco::PFCluster>& pfClusters,const std::vector<reco::SuperCluster>& scEB,const std::vector<reco::SuperCluster>& scEE);
void fillPFClustersHCAL(const SHEvent* event,double maxDR,SHPFClusterContainer& shPFClusters,const std::vector<reco::PFCluster>& pfClusters);
int getSCSeedCrysId(uint pfSeedId,const std::vector<reco::SuperCluster>& superClusters);

void dumpPFInfo(const edm::ValueMap<std::vector<reco::PFCandidateRef> >& isoMaps,const edm::Handle<std::vector<reco::GsfElectron> >& eleHandle);

void SHNtupliser::initSHEvent()
{
  if(shEvt_) delete shEvt_;
  shEvt_ = new SHEvent;
}

void SHNtupliser::fillTree()
{
  evtTree_->Fill();
}

SHNtupliser::SHNtupliser(const edm::ParameterSet& iPara):
  evtHelper_(),heepEvt_(),shEvtHelper_(),shEvt_(NULL),evtTree_(NULL),outFile_(NULL),nrTot_(0),nrPass_(0),initGeom_(false),puSummary_(NULL),writePUInfo_(true),shPFCands_(NULL),shPFClusters_(NULL)
{
  evtHelper_.setup(iPara,consumesCollector(),*this);
  shEvtHelper_.setup(iPara);

  outputFilename_ = iPara.getParameter<std::string>("outputFilename");
  
  double eventWeight = iPara.getParameter<double>("sampleWeight");
  int datasetCode = iPara.getParameter<int>("datasetCode");  
  outputGeom_ = iPara.getParameter<bool>("outputGeom");
   
  minSCEtToPass_ = iPara.getParameter<double>("minSCEtToPass");
  minNrSCToPass_ = iPara.getParameter<int>("minNrSCToPass");
  
  minJetEtToPass_ = iPara.getParameter<double>("minJetEtToPass");
  minNrJetToPass_ = iPara.getParameter<int>("minNrJetToPass");
  
  shEvtHelper_.setDatasetCode(datasetCode);
  shEvtHelper_.setEventWeight(eventWeight);
 
 
  hltTag_ = iPara.getParameter<std::string>("hltProcName");
  addCaloTowers_ = iPara.getParameter<bool>("addCaloTowers");
  addCaloHits_ = iPara.getParameter<bool>("addCaloHits");
  addPFCands_=iPara.getParameter<bool>("addPFCands"); 
  addPFClusters_=iPara.getParameter<bool>("addPFClusters");
  addIsolTrks_ = iPara.getParameter<bool>("addIsolTrks");
  addPreShowerClusters_ = false;
  addGenInfo_ = true;
  writePUInfo_ = iPara.getParameter<bool>("writePUInfo");

}

SHNtupliser::~SHNtupliser()
{
  if(shEvt_) delete shEvt_;
  if(puSummary_) delete puSummary_;
  if(shPFCands_) delete shPFCands_;
  if(shPFClusters_) delete shPFClusters_;
}

void SHNtupliser::beginJob()
{
  initSHEvent();
  shCaloTowers_ = &(shEvt_->getCaloTowers());
  shCaloHits_= &(shEvt_->getCaloHits());
  shIsolTrks_= &(shEvt_->getIsolTrks());
  shPreShowerClusters_ = &(shEvt_->getPreShowerClusters());
  shGenInfo_ = &(shEvt_->getGenInfo());
  shTrigSum_ = &(shEvt_->getTrigSum());
  std::cout <<"opening file "<<outputFilename_.c_str()<<std::endl;

  edm::Service<TFileService> fs;
  outFile_ = &fs->file();
  outFile_->cd();
  evtTree_= new TTree("evtTree","Event Tree");
 
  int splitLevel=2;
  evtTree_->SetCacheSize(1024*1024*100);
					       
  evtTree_->Branch("EventBranch",shEvt_->GetName(),&shEvt_,32000,splitLevel);
  evtTree_->Branch("TrigSummaryBranch","SHTrigSummary",&shTrigSum_,32000,splitLevel);
  if(writePUInfo_) {
    puSummary_ = new SHPileUpSummary;
    evtTree_->Branch("PUInfoBranch","SHPileUpSummary",&puSummary_,32000,splitLevel);
  }
  if(addCaloTowers_) {
    evtTree_->Branch("CaloTowersBranch","SHCaloTowerContainer",&shCaloTowers_,32000,splitLevel);
  }
  if(addCaloHits_){
    evtTree_->Branch("CaloHitsBranch","SHCaloHitContainer",&shCaloHits_,32000,splitLevel);
  }
  if(addIsolTrks_){
    evtTree_->Branch("IsolTrksBranch","TClonesArray",&shIsolTrks_,32000,splitLevel);
  }
  if(addPreShowerClusters_){
    evtTree_->Branch("PreShowerClustersBranch","TClonesArray",&shPreShowerClusters_,32000,splitLevel);
  }
  if(addGenInfo_){
    evtTree_->Branch("GenInfoBranch","SHGenInfo",&shGenInfo_,32000,splitLevel);
  }

  if(addPFCands_){ 
    shPFCands_ = new SHPFCandContainer;
    evtTree_->Branch("PFCandsBranch","SHPFCandContainer",&shPFCands_,32000,splitLevel);
  }
  if(addPFClusters_){ 
    shPFClusters_= new SHPFClusterContainer;
    evtTree_->Branch("PFClustersBranch","SHPFClusterContainer",&shPFClusters_,32000,splitLevel);
  }
 
} 

void SHNtupliser::beginRun(const edm::Run& run,const edm::EventSetup& iSetup)
{ 
  std::cout <<"begin run "<<initGeom_<<std::endl;
  if(!initGeom_){
  //write out calogeometry
   
    SHGeomFiller geomFiller(iSetup);  
    SHCaloGeom ecalGeom(SHCaloGeom::ECAL);
    SHCaloGeom hcalGeom(SHCaloGeom::HCAL);
    geomFiller.fillEcalGeom(ecalGeom);
    geomFiller.fillHcalGeom(hcalGeom);
    if(outputGeom_){
      std::cout <<"writing geom "<<std::endl;
      outFile_->WriteObject(&ecalGeom,"ecalGeom");
      outFile_->WriteObject(&hcalGeom,"hcalGeom");
    }
    GeomFuncs::loadCaloGeom(ecalGeom,hcalGeom);
    initGeom_=true;
  }
  evtHelper_.makeHeepEvent(run,iSetup,heepEvt_);
  std::cout <<"end begin run "<<std::endl;


}

void SHNtupliser::analyze(const edm::Event& iEvent,const edm::EventSetup& iSetup)
{
  
  if(fillSHEvent(iEvent,iSetup)) evtTree_->Fill();
}

bool SHNtupliser::fillSHEvent(const edm::Event& iEvent,const edm::EventSetup& iSetup)
{
  //std::cout <<"heep eventing" <<std::endl;
  evtHelper_.makeHeepEvent(iEvent,iSetup,heepEvt_);
 
  //even easier to convert from heep to shEvt
  //std::cout <<"converting eventing" <<std::endl;
  
  nrTot_++;
 
  
  shEvtHelper_.makeSHEvent(heepEvt_,*shEvt_);
  SHTrigSumMaker::makeSHTrigSum(heepEvt_,*shTrigSum_);
  if(addGenInfo_) GenFuncs::fillGenInfo(heepEvt_,*shGenInfo_);

  if(addPFCands_) shPFCands_->clear();
  if(addPFClusters_) shPFClusters_->clear();
  if(heepEvt_.handles().vertices.isValid()){
    reco::VertexRef mainVtx(heepEvt_.handles().vertices,0);
    if(addPFCands_ && 
       heepEvt_.handles().pfCandidate.isValid() &&
       heepEvt_.handles().gsfEle.isValid() && 
       heepEvt_.handles().gsfEleToPFCandMap.isValid()){
      PFFuncs::fillPFCands(shEvt_,0.5,*shPFCands_,heepEvt_.handles().pfCandidate,
			   mainVtx,heepEvt_.handles().vertices,
			   *(heepEvt_.handles().gsfEleToPFCandMap.product()),
			   heepEvt_.handles().gsfEle);
    }
  }

  if(addPFClusters_ && heepEvt_.handles().pfClustersECAL.isValid() && heepEvt_.handles().pfClustersHCAL.isValid() &&
     heepEvt_.handles().superClusEB.isValid() && heepEvt_.handles().superClusEE.isValid()){
    fillPFClustersECAL(shEvt_,0.5,*shPFClusters_,heepEvt_.pfClustersECAL(),heepEvt_.superClustersEB(),heepEvt_.superClustersEE());
    fillPFClustersHCAL(shEvt_,0.5,*shPFClusters_,heepEvt_.pfClustersHCAL());
  }


  if(writePUInfo_){ //naughty but its almost 1am...
    puSummary_->clear();
    if(heepEvt_.handles().pileUpMCInfo.isValid()){
      for(auto& puInfo : *heepEvt_.handles().pileUpMCInfo){
	puSummary_->addPUInfo( puInfo.getBunchCrossing(),puInfo.getPU_NumInteractions(),puInfo.getTrueNumInteractions());
      }
    }
  }
  
  SHCaloHitContainer outputHits;
  filterHcalHits(shEvt_,0.5,shEvt_->getCaloHits(),outputHits);  
  filterEcalHits(shEvt_,0.5,shEvt_->getCaloHits(),outputHits);
  shEvt_->addCaloHits(outputHits);
    
  return true;

}


void dumpPFInfo(const edm::ValueMap<std::vector<reco::PFCandidateRef> > & isoMaps,const edm::Handle<std::vector<reco::GsfElectron> >& eleHandle)
{
  for(size_t eleNr=0;eleNr<eleHandle->size();eleNr++){
    reco::GsfElectronRef ele(eleHandle,eleNr);
    const std::vector<reco::PFCandidateRef>& isoCands =  isoMaps[ele];
    std::cout <<"electron "<<eleNr<<" et "<<ele->et()<<" eta "<<ele->eta()<<std::endl;
    for(size_t candNr=0;candNr<isoCands.size();candNr++){
      std::cout <<"cand "<<candNr<<" / "<<isoCands.size()<<" "<<(*isoCands[candNr])<<std::endl;
    }
  }
  
}




#include "SimDataFormats/GeneratorProducts/interface/GenRunInfoProduct.h"
void SHNtupliser::endRun(edm::Run const& iRun, edm::EventSetup const&)
{
  // edm::Handle< GenRunInfoProduct > genInfoProduct;
  // iRun.getByLabel("generator", genInfoProduct );
  // if(genInfoProduct.isValid()) {
  //   std::cout <<" cross-section "<<genInfoProduct->internalXSec().value()<<std::endl;
  // }
  
}


void SHNtupliser::endJob()
{ 
  outFile_->cd();
  //quick and dirty hack as writing ints directly isnt working
  TTree* tree = new TTree("eventCountTree","Event count");
  tree->Branch("nrPass",&nrPass_,"nrPass/I");
  tree->Branch("nrTot",&nrTot_,"nrTot/I");
  tree->Fill();

  std::cout <<"job ended "<<std::endl;
}

void filterHcalHits(const SHEvent* event,double maxDR,const SHCaloHitContainer& inputHits,SHCaloHitContainer& outputHits)
{

  std::vector<std::pair<float,float> > eleEtaPhi;
  for(int eleNr=0;eleNr<event->nrElectrons();eleNr++){
    const SHElectron* ele = event->getElectron(eleNr);
    eleEtaPhi.push_back(std::make_pair(ele->detEta(),ele->detPhi()));
  }
  
  // outputHits.clear();
  double maxDR2 = maxDR*maxDR;
  for(size_t hitNr=0;hitNr<inputHits.nrHcalHitsStored();hitNr++){
    int detId = inputHits.getHcalHitByIndx(hitNr).detId();
    double cellEta=0,cellPhi=0;
    GeomFuncs::getCellEtaPhi(detId,cellEta,cellPhi);
    
    bool accept =false;
    for(size_t eleNr=0;eleNr<eleEtaPhi.size();eleNr++){
      if(MathFuncs::calDeltaR2(eleEtaPhi[eleNr].first,eleEtaPhi[eleNr].second,
			       cellEta,cellPhi)<maxDR2){
	accept=true;
	break;
      }
    }//end ele loop
    if(accept) outputHits.addHit(inputHits.getHcalHitByIndx(hitNr));
    
  }//end hit loop


}

void filterEcalHits(const SHEvent* event,double maxDR,const SHCaloHitContainer& inputHits,SHCaloHitContainer& outputHits)
{

  std::vector<std::pair<float,float> > eleEtaPhi;
  for(int eleNr=0;eleNr<event->nrElectrons();eleNr++){
    const SHElectron* ele = event->getElectron(eleNr);
    eleEtaPhi.push_back(std::make_pair(ele->detEta(),ele->detPhi()));
  }
  
  //outputHits.clear();
  double maxDR2 = maxDR*maxDR;
  for(size_t hitNr=0;hitNr<inputHits.nrEcalHitsStored();hitNr++){
    int detId = inputHits.getEcalHitByIndx(hitNr).detId();
    double cellEta=0,cellPhi=0;
    GeomFuncs::getCellEtaPhi(detId,cellEta,cellPhi);
    
    bool accept =false;
    for(size_t eleNr=0;eleNr<eleEtaPhi.size();eleNr++){
      if(MathFuncs::calDeltaR2(eleEtaPhi[eleNr].first,eleEtaPhi[eleNr].second,
			       cellEta,cellPhi)<maxDR2){
	accept=true;
	break;
      }
    }//end ele loop
    if(accept) outputHits.addHit(inputHits.getEcalHitByIndx(hitNr));
    
  }//end hit loop


}
  
void filterCaloTowers(const SHEvent* event,double maxDR,const SHCaloTowerContainer& inputHits,SHCaloTowerContainer& outputHits)
{

  std::vector<std::pair<float,float> > eleEtaPhi;
  for(int eleNr=0;eleNr<event->nrElectrons();eleNr++){
    const SHElectron* ele = event->getElectron(eleNr);
    eleEtaPhi.push_back(std::make_pair(ele->detEta(),ele->detPhi()));
  }
  
  outputHits.clear();
  double maxDR2 = maxDR*maxDR;
  for(size_t hitNr=0;hitNr<inputHits.nrCaloTowersStored();hitNr++){
    float towerEta = inputHits.getCaloTowerByIndx(hitNr).eta();
    float towerPhi = inputHits.getCaloTowerByIndx(hitNr).phi(); 
  
    bool accept =false;
    for(size_t eleNr=0;eleNr<eleEtaPhi.size();eleNr++){
      if(MathFuncs::calDeltaR2(eleEtaPhi[eleNr].first,eleEtaPhi[eleNr].second,
			       towerEta,towerPhi)<maxDR2){
	accept=true;
	break;
      }
    }//end ele loop
    if(accept) outputHits.addTower(inputHits.getCaloTowerByIndx(hitNr));
    
  }//end hit loop


}


void addPFClustersVec(std::vector<const reco::CaloCluster*>& clus,const std::vector<reco::SuperCluster>& scs)
{
  for(auto& sc : scs){
    for(reco::CaloCluster_iterator clusIt  = sc.clustersBegin();clusIt!=sc.clustersEnd();++clusIt){

      //    const reco::PFCluster* pfClus = dynamic_cast<const reco::PFCluster*>(&**clusIt);
      // std::cout<<typeid(**clusIt).name()<<" pf "<<pfClus<<std::endl;
      clus.push_back((&**clusIt));
    }
  }
}

void fillPFClustersECAL(const SHEvent* event,double maxDR,SHPFClusterContainer& shPFClusters,
		    const std::vector<reco::PFCluster>& pfClusters,
		    const std::vector<reco::SuperCluster>& superClustersEB,const std::vector<reco::SuperCluster>& superClustersEE)
{
  //  std::cout <<"filling candidates "<<std::endl;

  const double maxDR2 = maxDR*maxDR;
  std::vector<std::pair<float,float> > eleEtaPhi;
  for(int eleNr=0;eleNr<event->nrElectrons();eleNr++){
    const SHElectron* ele = event->getElectron(eleNr);
    if(ele->et()>20){
      eleEtaPhi.push_back(std::make_pair(ele->detEta(),ele->detPhi()));
    }
  }

  for(size_t clusNr=0;clusNr<pfClusters.size();clusNr++){
    const reco::PFCluster& pfCluster = pfClusters[clusNr];
   
    bool accept =false;
    for(size_t eleNr=0;eleNr<eleEtaPhi.size();eleNr++){
      if(MathFuncs::calDeltaR2(eleEtaPhi[eleNr].first,eleEtaPhi[eleNr].second,
			       pfCluster.eta(),pfCluster.phi())<maxDR2){
	accept=true;
	break;
      }
    }//end ele loop

    if(accept){
      const std::vector<reco::SuperCluster>& superClusters = pfCluster.caloID().detector(reco::CaloID::DET_ECAL_BARREL) ? superClustersEB : superClustersEE;
      //std::cout <<" pf clus E "<<pfCluster.energy()<<" eta "<<pfCluster.eta()<<" phi "<<pfCluster.phi()<<" seed "<<pfCluster.seed().rawId()<<" address "<<&pfCluster<<std::endl;
      //int scSeedCrysId=0;
      int scSeedCrysId=getSCSeedCrysId(pfCluster.seed().rawId(),superClusters);
      shPFClusters.addECALCluster(SHPFCluster(pfCluster,scSeedCrysId));
    } 
  }
}
void fillPFClustersHCAL(const SHEvent* event,double maxDR,SHPFClusterContainer& shPFClusters,const std::vector<reco::PFCluster>& pfClusters)
{
  //  std::cout <<"filling candidates "<<std::endl;

  const double maxDR2 = maxDR*maxDR;
  std::vector<std::pair<float,float> > eleEtaPhi;
  for(int eleNr=0;eleNr<event->nrElectrons();eleNr++){
    const SHElectron* ele = event->getElectron(eleNr);
    if(ele->et()>20){
      eleEtaPhi.push_back(std::make_pair(ele->detEta(),ele->detPhi()));
    }
  }

  for(size_t clusNr=0;clusNr<pfClusters.size();clusNr++){
    const reco::PFCluster& pfCluster = pfClusters[clusNr];

    bool accept =false;
    for(size_t eleNr=0;eleNr<eleEtaPhi.size();eleNr++){
      if(MathFuncs::calDeltaR2(eleEtaPhi[eleNr].first,eleEtaPhi[eleNr].second,
			       pfCluster.eta(),pfCluster.phi())<maxDR2){
	accept=true;
	break;
      }
    }//end ele loop

    if(accept){
      shPFClusters.addHCALCluster(SHPFCluster(pfCluster,0));
    } 
  }
}

int getSCSeedCrysId(uint pfSeedId,const std::vector<reco::SuperCluster>& superClusters)
{
  // std::cout <<"getting sc seed id "<<std::endl;
  for(size_t scNr=0;scNr<superClusters.size();scNr++){
    // std::cout <<"super clust "<<scNr<<" / "<<superClusters.size()<<std::endl;
    const reco::SuperCluster& sc = superClusters[scNr];
    for(reco::CaloCluster_iterator clusIt  = sc.clustersBegin();clusIt!=sc.clustersEnd();++clusIt){
      //  std::cout <<"clus seed E "<<(*clusIt)->energy()<<" eta "<<(*clusIt)->eta()<<" phi "<<(*clusIt)->phi()<<" "<<(*clusIt)->seed().rawId()<<" pf seed "<<pfSeedId<<" address "<<(&**clusIt)<<std::endl;
      if((*clusIt)->seed().rawId()==pfSeedId) return sc.seed()->seed().rawId();
    }
  }
  return 0;
}


//define this as a plug-in
DEFINE_FWK_MODULE(SHNtupliser);
