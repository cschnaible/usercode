#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "SHarper/SHNtupliser/interface/SHEventTreeData.h"

void SHEventTreeData::BranchData::setup(const edm::ParameterSet& iPara)
{
  addPFCands=iPara.getParameter<bool>("addPFCands");
  addPFClusters=iPara.getParameter<bool>("addPFClusters");
  addCaloTowers=iPara.getParameter<bool>("addCaloTowers");
  addCaloHits=iPara.getParameter<bool>("addCaloHits");
  addIsolTrks=iPara.getParameter<bool>("addIsolTrks");
  addPreShowerClusters=iPara.getParameter<bool>("addPreShowerClusters");
  addGenInfo=iPara.getParameter<bool>("addGenInfo");
  addPUInfo=iPara.getParameter<bool>("addPUInfo");
  addTrigSum=iPara.getParameter<bool>("addTrigSum");
  addMet=iPara.getParameter<bool>("addMet");
  addJets=iPara.getParameter<bool>("addJets");
  addMuons=iPara.getParameter<bool>("addMuons");
  addSuperClus=iPara.getParameter<bool>("addSuperClus");
  addEles=iPara.getParameter<bool>("addEles");
  addHLTDebug=iPara.getParameter<bool>("addHLTDebug");
  addMCParts=iPara.getParameter<bool>("addMCParts");
  addGainSwitchInfo=iPara.getParameter<bool>("addGainSwitchInfo");
  filterIsolTrks=iPara.getParameter<bool>("filterIsolTrks");
  filterEcalHits=iPara.getParameter<bool>("filterEcalHits");
  filterHcalHits=iPara.getParameter<bool>("filterHcalHits");
  filterCaloTowers=iPara.getParameter<bool>("filterCaloTowers");
  
}

SHEventTreeData::SHEventTreeData(SHEvent* & event):
  tree_(nullptr),
  event_(event),
  shPUSum_(nullptr),
  shPFCands_(nullptr),
  shPFClusters_(nullptr),
  shCaloTowers_(nullptr),
  shCaloHits_(nullptr),
  shIsolTrks_(nullptr),
  shPreShowerClusters_(nullptr),
  shGenInfo_(nullptr), 
  shTrigSum_(nullptr),
  shGSInfo_(nullptr)
{
  if(event_) setMemLocs();

}

void SHEventTreeData::setMemLocs()
{
  shPUSum_ = &(event_->getPUSum());
  shPFCands_ = &(event_->getPFCands());
  shPFClusters_ = &(event_->getPFClusters());
  shCaloTowers_ = &(event_->getCaloTowers());
  shCaloHits_ = &(event_->getCaloHits());
  shIsolTrks_ = &(event_->getIsolTrks());
  shPreShowerClusters_ = &(event_->getPreShowerClusters());
  shGenInfo_ = &(event_->getGenInfo()); 
  shTrigSum_ = &(event_->getTrigSum());
  shGSInfo_ = &(event_->getGSInfo());
}

void SHEventTreeData::makeTree(const std::string& name)
{  
  setMemLocs();

  tree_= new TTree(name.c_str(),"Event Tree");
  int splitLevel=2;
  tree_->SetCacheSize(1024*1024*100);
					       
  tree_->Branch("EventBranch",event_->GetName(),&event_,32000,splitLevel);
  if(branches_.addPFCands) tree_->Branch("PFCandsBranch","SHPFCandContainer",&shPFCands_,32000,splitLevel);
  if(branches_.addPFClusters) tree_->Branch("PFClustersBranch","SHPFClusterContainer",&shPFClusters_,32000,splitLevel);
  if(branches_.addCaloTowers) tree_->Branch("CaloTowersBranch","SHCaloTowerContainer",&shCaloTowers_,32000,splitLevel);
  if(branches_.addCaloHits) tree_->Branch("CaloHitsBranch","SHCaloHitContainer",&shCaloHits_,32000,splitLevel);
  if(branches_.addIsolTrks) tree_->Branch("IsolTrksBranch","TClonesArray",&shIsolTrks_,32000,splitLevel);
  if(branches_.addPreShowerClusters) tree_->Branch("PreShowerClustersBranch","TClonesArray",&shPreShowerClusters_,32000,splitLevel);
  if(branches_.addGenInfo) tree_->Branch("GenInfoBranch","SHGenInfo",&shGenInfo_,32000,splitLevel);
  if(branches_.addPUInfo) tree_->Branch("PUInfoBranch","SHPileUpSummary",&shPUSum_,32000,splitLevel);
  if(branches_.addTrigSum) tree_->Branch("TrigSummaryBranch","SHTrigSummary",&shTrigSum_,32000,splitLevel);
  if(branches_.addGainSwitchInfo) tree_->Branch("GainSwitchInfoBranch","SHGainSwitchInfo",&shGSInfo_,32000,splitLevel);
}

void SHEventTreeData::fill()
{
  //menu is not already stored in the manager, add it (first check we have a menu to  store though)
  if(shTrigSum_->hltMenu() && 
     !trigMenuMgr_.getHLT(shTrigSum_->menuName(),shTrigSum_->processName()).valid()) {
    trigMenuMgr_.add(*shTrigSum_->hltMenu());
  }
  if(shTrigSum_->l1Menu() && 
     !trigMenuMgr_.getL1(shTrigSum_->l1MenuName()).valid()) {
    trigMenuMgr_.add(*shTrigSum_->l1Menu());
  }
  trigMenuMgr_.write(tree_);
  shTrigSum_->clearMenuData(); 
  tree_->Fill();
}
