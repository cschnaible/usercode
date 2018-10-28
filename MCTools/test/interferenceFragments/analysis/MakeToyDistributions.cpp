// Hypothesis testing between Z'/Z/g interference & peak and Z/g only.
// Edited 23 October 2018
// New version to store tree of toys
// Chris Schnaible 21 Aug 2018
//
#include <vector>
#include <string>
using namespace RooFit;

void MakeToyDistributions(
    TString model,TString channel,TString mass,bool add2017=false,
    int NPE = 5000, double MMIN=600, double MMAX=9000,
    TString PDF,
    TString extraName, TString inputDateString
    ) 
{
    RooMsgService::instance().setGlobalKillBelow(RooFit::WARNING);
    gStyle->SetLegendBorderSize(0);
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    //gStyle->SetOptStat(0);
    gStyle->SetOptTitle(0);
    gStyle->SetTitleStyle(0);

    TString ZPrimeModelHistName = "ZPrime";
    ZPrimeModelHistName.Append(model);ZPrimeModelHistName.Append("To");
    ZPrimeModelHistName.Append(channel);ZPrimeModelHistName.Append("_ResM");
    ZPrimeModelHistName.Append(mass);ZPrimeModelHistName.Append("_Int");
    ZPrimeModelHistName.Append("_");ZPrimeModelHistName.Append(PDF);
    // Calculate stuff with real data
    TString dataFile = "";
    int nData = -1;
    if (channel=="MuMu") {
        if (add2017==false) {
            dataFile.Append("data/data_Run2016_All_07Aug2017_list_sort_m600.txt");
            nData = 1601;
        }
        else {
            dataFile.Append("data/data_Run2016_07Aug2017_Run2017_17Nov2017_list_sort_m600.txt");
            nData = 3678;
        }
    }
    else if (channel=="EE") {
        if (add2017==false) {
            dataFile.Append("data/data_Run2016_dielectron_all_sort_m600.txt");
            nData = 1167;
        }
        else{
            dataFile.Append("data/data_Run2016_Run2017_dielectron_all_sort_m600.txt");
            nData = 2520;
        }
    }
    else {
        std::cout << channel << " wrong channel?" << std::endl;
        return;
    }
    std::cout << ZPrimeModelHistName << std::endl;
    std::cout << "Number of pseudoexperiments : " << NPE << std::endl;
    std::cout << "Number of events : " << nData << std::endl;
    std::cout << "Mass range : [" << MMIN << " ," << MMAX << "]" << std::endl;
    std::cout << "**********" << std::endl;

    TFile *sbfile = TFile::Open("root/ZprimeInterferenceHists_ZPrime"+model+"_"+mass+"_"+PDF+"_"+inputDateString+".root");
    TH1F *sbhist_th1 = (TH1F*)sbfile->Get(ZPrimeModelHistName)->Clone();
    sbhist_th1->SetDirectory(0);
    sbfile->Close();
    TFile *bfile = TFile::Open("root/ZprimeInterferenceHists_DY_"+PDF+"_"+inputDateString+".root");
    TH1F *bhist_th1 = (TH1F*)bfile->Get("DYTo"+channel+"_"+PDF)->Clone();
    bhist_th1->SetDirectory(0);
    bfile->Close();

    TString outFileName = ZPrimeModelHistName;
    outFileName.Append("_NPE_");outFileName.Append(Form("%d",NPE));
    outFileName.Append("_NEVT_");outFileName.Append(Form("%d",nData));
    outFileName.Append("_M_");outFileName.Append(Form("%d",(int)MMIN));outFileName.Append("_");
    outFileName.Append(Form("%d",(int)MMAX));outFileName.Append("_toys_");
    outFileName.Append(extraName);outFileName.Append(".root");
    std::cout << outFileName << std::endl;
    TFile *outFile = TFile::Open("hists/"+extraName+"/"+outFileName,"recreate");
    outFile->cd();
    sbhist_th1->Write();
    bhist_th1->Write();
    

    RooRealVar m("m","mass",MMIN,MMAX);
    RooDataHist sbhist("sbhist","sbhist",m,sbhist_th1);
    RooHistPdf sbpdf("sbpdf","sbpdf",m,sbhist,0);
    RooDataHist bhist("bhist","bhist",m,bhist_th1);
    RooHistPdf bpdf("bpdf","bpdf",m,bhist,0);

    RooDataSet* data = RooDataSet::read(dataFile,m);

    RooMCStudy *sbstudy = new RooMCStudy(sbpdf,m,Binned(kFALSE),Silence(kTRUE));
    RooMCStudy *bstudy = new RooMCStudy(bpdf,m,Binned(kFALSE),Silence(kTRUE));

    sbstudy->generate(NPE,nEvtPerSample=nData,keepGenData=kTRUE);
    bstudy->generate(NPE,nEvtPerSample=nData,keepGenData=kTRUE);

    /*
     * For every pseudo-experiment calculate the likelihood ratio and 
     * fill a histogram.
     * For every individual event in the pseudo-experiment calculate
     * the likelihood ratio and fill a histogram.
     * For the first pseudo-experiment save the generated pseudo data and
     * plot it with the PDF that generated the data.
     */
    for (int pe = 0; pe < NPE; pe++) {

        TString thisTreeName = "peData";
        thisTreeName.Append(Form("%d",pe));
        TTree *peTree = new TTree(thisTreeName,"PE data");

        double mass_sb;
        peTree->Branch("mass_sb",&mass_sb,"mass_sb/D");
        double mass_b;
        peTree->Branch("mass_b",&mass_b,"mass_b/D");
        double nll_sb;
        peTree->Branch("nll_sb",&nll_sb,"nll_sb/D");
        double nll_b;
        peTree->Branch("nll_b",&nll_b,"nll_b/D");

        RooNLLVar sbnll_d("sbnll_d","sbnll_d",sbpdf,*data);
        RooNLLVar bnll_d("bnll_d","bnll_d",bpdf,*data);
        double lambda_d = 2*(sbnll_d.getVal() - bnll_d.getVal());
        TParameter<double>* lambda_data = new TParameter<double>("lambda_d",-999);
        lambda_data->SetVal(lambda_d);
        peTree->GetUserInfo()->Add(lambda_data);
        
        RooDataSet *sbdata = sbstudy->genData(pe);
        // calculate L(S+B)
        RooNLLVar sbnll_sb("sbnll_sb","sbnll_sb",sbpdf,*sbdata);
        // calculate L(B)
        RooNLLVar bnll_sb("bnll_sb","bnll_sb",bpdf,*sbdata);
        // calculate lambda_SB = -2*log( L(S+B) / L(B) )
        // dont need extra negative sign since nll is already negative!
        double lambda_sb_val = 2*(sbnll_sb.getVal() - bnll_sb.getVal());

        TParameter<double>* lambda_sb = new TParameter<double>("lambda_sb",-999);
        lambda_sb->SetVal(lambda_sb_val);
        peTree->GetUserInfo()->Add(lambda_sb);

        RooDataSet *bdata = bstudy->genData(pe);
        // calculate L(S+B)
        RooNLLVar sbnll_b("sbnll_b","sbnll_b",sbpdf,*bdata);
        // calculate L(B)
        RooNLLVar bnll_b("bnll_b","bnll_b",bpdf,*bdata);
        // calculate lambda_SB = -2*log( L(S+B) / L(B) )
        // dont need extra negative sign since nll is already negative!
        double lambda_b_val = 2*(sbnll_b.getVal() - bnll_b.getVal());

        TParameter<double>* lambda_b = new TParameter<double>("lambda_b",-999);
        lambda_b->SetVal(lambda_b_val);
        peTree->GetUserInfo()->Add(lambda_b);

        RooArgSet* sbpdfobs_sb = sbpdf.getObservables(sbdata);
        RooArgSet* bpdfobs_sb = bpdf.getObservables(sbdata);
        RooArgSet* sbpdfobs_b = sbpdf.getObservables(bdata);
        RooArgSet* bpdfobs_b = bpdf.getObservables(bdata);

        for (int d=0; d<nData; d++) {
            *sbpdfobs_sb = *sbdata->get(d);
            *bpdfobs_sb = *sbdata->get(d);
            mass_sb = (*sbpdfobs_sb).getRealValue("m");

            *sbpdfobs_b = *bdata->get(d);
            *bpdfobs_b = *bdata->get(d);
            mass_b = (*bpdfobs_b).getRealValue("m");

            // I guess code==2 works
            double sbpdfval_sb = sbpdf.getVal()/sbpdf.analyticalIntegral(2);
            double bpdfval_sb = bpdf.getVal()/bpdf.analyticalIntegral(2);
            nll_sb = -2*(log(sbpdfval_sb)-log(bpdfval_sb));

            // I guess code==2 works
            double sbpdfval_b = sbpdf.getVal()/sbpdf.analyticalIntegral(2);
            double bpdfval_b = bpdf.getVal()/bpdf.analyticalIntegral(2);
            nll_b = -2*(log(sbpdfval_b)-log(bpdfval_b));

            peTree->Fill();
        }
        peTree->Write();
    }
    outFile->cd();
    outFile->Close();
    delete outFile;
    std::cout << std::endl;

}

