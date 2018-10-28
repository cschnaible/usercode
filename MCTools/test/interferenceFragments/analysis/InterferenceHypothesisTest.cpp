// Hypothesis testing between Z'/Z/g interference & peak and Z/g only.
// Chris Schnaible 21 Aug 2018
//
#include <vector>
#include <string>
using namespace RooFit;

void InterferenceHypothesisTest_new(
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
    outFileName.Append(Form("%d",(int)MMAX));outFileName.Append("_");
    outFileName.Append(extraName);outFileName.Append(".root");
    std::cout << outFileName << std::endl;
    TFile *outFile = TFile::Open("hists/"+extraName+"/"+outFileName,"recreate");
    outFile->cd();
    sbhist_th1->Write();
    //shist_th1->Write();
    bhist_th1->Write();

    TTree *peData = new TTree("peData","PE data");
    double lambda_sb_pe;
    double lambda_b_pe;
    peData->Branch("lambda_sb_pe",&lambda_sb_pe,"lambda_sb_pe/D");
    peData->Branch("lambda_b_pe",&lambda_b_pe,"lambda_b_pe/D");
    

    RooRealVar m("m","mass",MMIN,MMAX);
    RooDataHist sbhist("sbhist","sbhist",m,sbhist_th1);
    RooHistPdf sbpdf("sbpdf","sbpdf",m,sbhist,0);
    RooDataHist bhist("bhist","bhist",m,bhist_th1);
    RooHistPdf bpdf("bpdf","bpdf",m,bhist,0);

    RooDataSet* data = RooDataSet::read(dataFile,m);
    RooNLLVar sbnll_d("sbnll_d","sbnll_d",sbpdf,*data);
    RooNLLVar bnll_d("bnll_d","bnll_d",bpdf,*data);
    double lambda_d = 2*(sbnll_d.getVal() - bnll_d.getVal());
    TParameter<double>* lambda_data = new TParameter<double>("lambda_d",-999);
    lambda_data->SetVal(lambda_d);
    peData->GetUserInfo()->Add(lambda_data);
    std::cout << "\nData -2 * ln (s+b / b) = " << lambda_d << "\n" << std::endl;
    TH1F *hist_nll_d = new TH1F(ZPrimeModelHistName+"_hist_nll_d","",800,-200,200);
    hist_nll_d->Fill(lambda_d);

    TH1F *hist_sb = new TH1F(ZPrimeModelHistName+"_hist_nll_pe_sb","hist_sb",8000,-1000,1000);
    TH1F *hist_b = new TH1F(ZPrimeModelHistName+"_hist_nll_pe_b","hist_b",8000,-1000,1000);
    
    TH1F *hist_nll_event_sb = new TH1F(ZPrimeModelHistName+"_hist_nll_event_sb","",2400,-30,30);
    TH1F *hist_nll_event_b = new TH1F(ZPrimeModelHistName+"_hist_nll_event_b","",2400,-30,30);

    RooMCStudy *sbstudy = new RooMCStudy(sbpdf,m,Binned(kFALSE),Silence(kTRUE));
    RooMCStudy *bstudy = new RooMCStudy(bpdf,m,Binned(kFALSE),Silence(kTRUE));
    /*
    RooMCStudy *sbstudy = new RooMCStudy(sbpdf_msb,msb,Binned(kFALSE),Silence(kTRUE),Extended(kTRUE));
    RooMCStudy *bstudy = new RooMCStudy(bpdf_mb,mb,Binned(kFALSE),Silence(kTRUE),Extended(kTRUE));
    */

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

        if (pe%100==0) std::cout << "Pseudo-experiment " << pe << std::endl;
        
        RooDataSet *sbdata = sbstudy->genData(pe);
        // calculate L(S+B)
        RooNLLVar sbnll_sb("sbnll_sb","sbnll_sb",sbpdf,*sbdata);
        // calculate L(B)
        RooNLLVar bnll_sb("bnll_sb","bnll_sb",bpdf,*sbdata);
        // calculate lambda_SB = -2*log( L(S+B) / L(B) )
        // dont need extra negative sign since nll is already negative!
        double lambda_sb = 2*(sbnll_sb.getVal() - bnll_sb.getVal());
        lambda_sb_pe = lambda_sb;
        // Fill per event log likelihood histogram
        RooArgSet* sbpdfobs_sb = sbpdf.getObservables(sbdata);
        RooArgSet* bpdfobs_sb = bpdf.getObservables(sbdata);
        /*
         * These lines cause a seg fault when I try to close outFile?
        if (pe<4) {
            //--------
            // Draw a sample pseudoexperiment
            // Signal + Background
            //RooArgSet* sbpdfobs_sb_test = sbpdf.getObservables(sbdata);
            TString canvName = ZPrimeModel+"_sb_PE";
            canvName.Append(Form("%d",pe+1));
            TString histName = ZPrimeModel+"_hist_sb_PE";
            histName.Append(Form("%d",pe+1));
            TH1F *sbdatapehist = new TH1F(histName,"",180,0,9000);
            for (int d=0; d<sbdata->numEntries(); d++) {
                *sbpdfobs_sb = *sbdata->get(d);
                sbdatapehist->Fill((*sbpdfobs_sb).getRealValue("m"));
            }
            //RooBinning b(0,9000);b.addUniform(180,0,9000);
            RooPlot* sbdataframe = m.frame();
            //sbdata->plotOn(sbdataframe,Binning(b));
            sbdataframe->addTH1(sbdatapehist,"pe");
            bpdf.plotOn(sbdataframe,LineColor(kBlue),Normalization(1601,RooAbsReal::NumEvent));
            sbpdf.plotOn(sbdataframe,LineColor(kRed),Normalization(1601,RooAbsReal::NumEvent));
            sbdataframe->addTH1(sbdatapehist,"pe");
            //sbdata->plotOn(sbdataframe,Binning(b));
            TCanvas* c1 = new TCanvas(canvName,"",900,600);
            gPad->SetLogy(1); gPad->SetLeftMargin(0.15);
            sbdataframe->GetYaxis()->SetTitleOffset(1.6);
            sbdataframe->Draw();
            sbdataframe->GetYaxis()->SetTitle("Events / 50 GeV");
            sbdataframe->GetYaxis()->SetRangeUser(1E-7,1E4);
            sbdatapehist->SetMarkerStyle(kFullCircle);
            c1->SaveAs("plots/"+canvName+"_20180922.pdf");
            c1->Write();
            delete c1;
        }
        */
        for (int d=0; d<sbdata->numEntries(); d++) {
            *sbpdfobs_sb = *sbdata->get(d);
            *bpdfobs_sb = *sbdata->get(d);

            // I guess code==2 works
            double sbpdfval_sb = sbpdf.getVal()/sbpdf.analyticalIntegral(2);
            double bpdfval_sb = bpdf.getVal()/bpdf.analyticalIntegral(2);
            hist_nll_event_sb->Fill(-2*(log(sbpdfval_sb)-log(bpdfval_sb)));
        }
        RooDataSet *bdata = bstudy->genData(pe);
        // calculate L(S+B)
        RooNLLVar sbnll_b("sbnll_b","sbnll_b",sbpdf,*bdata);
        // calculate L(B)
        RooNLLVar bnll_b("bnll_b","bnll_b",bpdf,*bdata);
        // calculate lambda_SB = -2*log( L(S+B) / L(B) )
        // dont need extra negative sign since nll is already negative!
        double lambda_b = 2*(sbnll_b.getVal() - bnll_b.getVal());
        lambda_b_pe = lambda_b;
        // Fill per event log likelihood histogram
        RooArgSet* sbpdfobs_b = sbpdf.getObservables(bdata);
        RooArgSet* bpdfobs_b = bpdf.getObservables(bdata);
        /*
         * These lines cause a seg fault when I try to close outFiel?
        if (pe<4) {
            //--------
            // Draw a sample pseudoexperiment
            // Background
            //RooArgSet* bpdfobs_b_test = bpdf.getObservables(bdata);
            TString canvName = ZPrimeModel+"_b_PE";
            canvName.Append(Form("%d",pe+1));
            TString histName = ZPrimeModel+"_hist_b_PE";
            histName.Append(Form("%d",pe+1));
            TH1F *bdatapehist = new TH1F(histName,"",180,0,9000);
            for (int d=0; d<bdata->numEntries(); d++) {
                *bpdfobs_b = *bdata->get(d);
                bdatapehist->Fill((*bpdfobs_b).getRealValue("m"));
            }
            //RooBinning b(0,9000);b.addUniform(180,0,9000);
            RooPlot *bdataframe = m.frame();
            //bdata->plotOn(bdataframe,Binning(b));
            bdataframe->addTH1(bdatapehist,"pe");
            sbpdf.plotOn(bdataframe,LineColor(kRed),Normalization(1601,RooAbsReal::NumEvent));
            bpdf.plotOn(bdataframe,LineColor(kBlue),Normalization(1601,RooAbsReal::NumEvent));
            bdataframe->addTH1(bdatapehist,"pe");
            //bdata->plotOn(bdataframe,Binning(b));
            TCanvas* c2 = new TCanvas(canvName,"",900,600);
            gPad->SetLogy(1); gPad->SetLeftMargin(0.15);
            bdataframe->GetYaxis()->SetTitleOffset(1.6); 
            bdataframe->Draw();
            bdatapehist->SetMarkerStyle(kFullCircle);
            bdataframe->GetYaxis()->SetTitle("Events / 50 GeV");
            bdataframe->GetYaxis()->SetRangeUser(1E-7,1E4);
            c2->SaveAs("plots/"+canvName+"_20180922.pdf");
            c2->Write();
            delete c2;
        }
        */
        for (int d=0; d<bdata->numEntries(); d++) {
            *sbpdfobs_b = *bdata->get(d);
            *bpdfobs_b = *bdata->get(d);

            // I guess code==2 works
            double sbpdfval_b = sbpdf.getVal()/sbpdf.analyticalIntegral(2);
            double bpdfval_b = bpdf.getVal()/bpdf.analyticalIntegral(2);
            hist_nll_event_b->Fill(-2*(log(sbpdfval_b)-log(bpdfval_b)));
        }
        hist_sb->Fill(lambda_sb);
        hist_b->Fill(lambda_b);
        peData->Fill();
    }
    outFile->cd();
    peData->Write();
    // Store histograms for later use
    hist_sb->Write();
    hist_b->Write();
    hist_nll_event_sb->Write();
    hist_nll_event_b->Write();
    hist_nll_d->Write();
    /*
    //--------
    // Draw per pseudoexperiment log likelihood ratio
    TCanvas *c = new TCanvas("c","",900,600);

    hist_sb->Draw();
    gPad->Update();
    TPaveStats *statbox_sb = (TPaveStats*)hist_sb->GetListOfFunctions()->FindObject("stats");
    statbox_sb->SetY1NDC(0.7);
    statbox_sb->SetY2NDC(0.7 + 0.15);

    hist_b->Draw();
    gPad->Update();
    TPaveStats *statbox_b = (TPaveStats*)hist_b->GetListOfFunctions()->FindObject("stats");
    statbox_b->SetY1NDC(0.7 - 0.15  - 0.025);
    statbox_b->SetY2NDC(0.7 - 0.15  - 0.025 + 0.15);

    TLegend *leg = new TLegend(0.2,0.7,0.3,0.85);
    leg->AddEntry(hist_sb,"S+B");
    leg->AddEntry(hist_b,"B");

    hist_sb->Draw();
    hist_b->Draw("same");
    statbox_sb->Draw("same");
    statbox_b->Draw("same");
    leg->Draw("same");

    hist_sb->SetLineColor(kOrange+1);
    hist_sb->SetLineWidth(2);
    hist_sb->GetXaxis()->SetTitle("-2 ln (L_{S+B} / L_{B})");
    hist_sb->GetXaxis()->CenterTitle();
    hist_sb->GetYaxis()->SetTitle("pseudoexperiments");
    hist_sb->GetYaxis()->CenterTitle();
    hist_b->SetLineColor(kBlue);
    hist_b->SetLineWidth(2);
    leg->SetFillStyle(0);
    leg->SetLineStyle(0);

    //c->SaveAs(ZPrimeModel+"_n2LL_test.pdf");
    outFile->cd();
    c->Write(ZPrimeModel+"_n2LL");
    delete c;

    //--------
    // Draw per event log likelihood ratio
    //--------
    // Signal + Background
    TCanvas *c3 = new TCanvas("c3","",900,600);
    hist_nll_event_sb->Draw("");
    hist_nll_event_sb->SetLineWidth(2);
    hist_nll_event_sb->GetXaxis()->SetTitle("-2 ln (L_{S+B} / L_{B})");
    hist_nll_event_sb->GetXaxis()->CenterTitle();
    hist_nll_event_sb->GetYaxis()->SetTitle("Events / 0.02");
    hist_nll_event_sb->GetYaxis()->CenterTitle();
    //c3->SaveAs(ZPrimeModel+"_n2ll_event_sb_test.pdf");
    outFile->cd();
    c3->Write(ZPrimeModel+"_n2ll_event_sb");
    delete c3;
    //--------
    // Background
    TCanvas *c4 = new TCanvas("c4","",900,600);
    hist_nll_event_b->Draw("");
    hist_nll_event_b->SetLineWidth(2);
    hist_nll_event_b->GetXaxis()->SetTitle("-2 ln (L_{S+B} / L_{B})");
    hist_nll_event_b->GetXaxis()->CenterTitle();
    hist_nll_event_b->GetYaxis()->SetTitle("Events / 0.02");
    hist_nll_event_b->GetYaxis()->CenterTitle();
    //c4->SaveAs(ZPrimeModel+"_n2ll_event_b_test.pdf");
    outFile->cd();
    c4->Write(ZPrimeModel+"_n2ll_event_b_test");
    delete c4;
    outFile->Write();
    */
    outFile->Close();
    delete outFile;
    std::cout << std::endl;

}

