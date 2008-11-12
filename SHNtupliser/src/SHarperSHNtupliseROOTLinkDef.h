#include "SHarper/SHNtupliser/interface/SHEvent.hh"
#include "SHarper/SHNtupliser/interface/SHCaloHit.hh"
#include "SHarper/SHNtupliser/interface/SHBasicCluster.hh"
#include "SHarper/SHNtupliser/interface/SHSuperCluster.hh"
#include "SHarper/SHNtupliser/interface/SHElectron.hh"
#include "SHarper/SHNtupliser/interface/SHMCParticle.hh"
#include "SHarper/SHNtupliser/interface/SHCaloHitContainer.hh"
#include "SHarper/SHNtupliser/interface/SHJet.hh"
#include "SHarper/SHNtupliser/interface/SHIsolCluster.hh"
#include "SHarper/SHNtupliser/interface/SHIsolSuperCluster.hh"
#include "SHarper/SHNtupliser/interface/SHIsolTrack.hh"
#include "SHarper/SHNtupliser/interface/SHTrigInfo.hh"
#include "SHarper/SHNtupliser/interface/SHMet.hh"
#include "SHarper/SHNtupliser/interface/SHCaloGeom.hh"
#include "SHarper/SHNtupliser/interface/SHCaloCellGeom.hh"
#ifdef __CINT__
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ class SHEvent+;

#pragma link C++ class SHCaloHit+;
#pragma link C++ class SHBasicCluster+;
#pragma link C++ class SHSuperCluster+; 
#pragma link C++ class SHElectron+;
#pragma link C++ class SHMCParticle+; 

                           
#pragma link C++ class SHCaloHitContainer+;
#pragma link C++ class SHJet+;
#pragma link C++ class SHIsolCluster+;
#pragma link C++ class SHIsolSuperCluster+; 
#pragma link C++ class SHIsolTrack+; 
#pragma link C++ class SHTrigInfo+;
#pragma link C++ class SHMet+;
#pragma link C++ class SHCaloGeom+;
#pragma link C++ class SHCaloCellGeom+; 
#pragma link C++ class SHCaloCellGeom::CellEdges+; 
#endif
