// Hypothesis testing between Z'/Z/g interference & peak and Z/g only.
// Chris Schnaible 21 Aug 2018
//
#include <vector>
#include <string>
using namespace RooFit;

void InterferenceHypothesisTest_test2(
    TString ZPrimeModel,int NPE = 1000,int DATAEVENTS = 3300, double MMIN=500, double MMAX=7000
    ) 
{
    gStyle->SetLegendBorderSize(0);
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    //gStyle->SetOptStat(0);
    gStyle->SetOptTitle(0);
    gStyle->SetTitleStyle(0);

    std::cout << ZPrimeModel << std::endl;
    std::cout << "Number of pseudoexperiments : " << NPE << std::endl;
    std::cout << "Number of events : " << DATAEVENTS << std::endl;
    std::cout << "Mass range : [" << MMIN << " ," << MMAX << "]" << std::endl;
    std::cout << "**********" << std::endl;

    TFile *f = TFile::Open("test.root");
    TH1F *bhist_th1 = (TH1F*)f->Get("DYToLL")->Clone();
    bhist_th1->SetDirectory(0);
    TH1F *sbhist_th1 = (TH1F*)f->Get(ZPrimeModel)->Clone();
    sbhist_th1->SetDirectory(0);

    RooRealVar m("m","mass",MMIN,MMAX);
    RooDataHist sbhist("sbhist","sbhist",m,sbhist_th1);
    RooHistPdf sbpdf("sbpdf","sbpdf",m,sbhist,0);
    RooDataHist bhist("bhist","bhist",m,bhist_th1);
    RooHistPdf bpdf("bpdf","bpdf",m,bhist,0);

    TH1F *hist_sb = new TH1F(ZPrimeModel+"_hist_sb","hist_sb",500,-100,100);
    TH1F *hist_b = new TH1F(ZPrimeModel+"_hist_b","hist_b",500,-100,100);
    
    TH1F *hist_nll_event_sb = new TH1F(ZPrimeModel+"_hist_nll_event_sb","",125,-0.5,2);
    TH1F *hist_nll_event_b = new TH1F(ZPrimeModel+"_hist_nll_event_b","",125,-0.5,2);

    RooMCStudy *sbstudy = new RooMCStudy(sbpdf,m,Binned(kFALSE),Silence(kTRUE));
    RooMCStudy *bstudy = new RooMCStudy(bpdf,m,Binned(kFALSE),Silence(kTRUE));
    /*
    RooMCStudy *sbstudy = new RooMCStudy(sbpdf_msb,msb,Binned(kFALSE),Silence(kTRUE),Extended(kTRUE));
    RooMCStudy *bstudy = new RooMCStudy(bpdf_mb,mb,Binned(kFALSE),Silence(kTRUE),Extended(kTRUE));
    */

    sbstudy->generate(NPE,nEvtPerSample=DATAEVENTS,keepGenData=kTRUE);
    bstudy->generate(NPE,nEvtPerSample=DATAEVENTS,keepGenData=kTRUE);

    for (int pe = 0; pe < NPE; pe++) {
        
        RooDataSet *sbdata = sbstudy->genData(pe);
        // calculate L(S+B)
        RooNLLVar sbnll_sb("sbnll_sb","sbnll_sb",sbpdf,*sbdata);
        // calculate L(B)
        RooNLLVar bnll_sb("bnll_sb","bnll_sb",bpdf,*sbdata);
        // calculate lambda_SB = -2*log( L(S+B) / L(B) )
        double lambda_sb = -2*(sbnll_sb.getVal() - bnll_sb.getVal());
        if (pe==0) {
            //--------
            // Draw a sample pseudoexperiment
            // Signal + Background
            RooPlot* sbframe = m.frame(Title("S+B pdf"));
            sbpdf.plotOn(sbframe);
            RooPlot* sbdataframe = m.frame(Title("S+B pdf with data"));
            sbdata->plotOn(sbdataframe);
            sbpdf.plotOn(sbdataframe);
            bpdf.plotOn(sbdataframe);
            TCanvas* c1 = new TCanvas("sb_PE1","sb_PE1",800,400);
            c1->Divide(2);
            c1->cd(1); gPad->SetLogy(1); gPad->SetLeftMargin(0.15);
            sbframe->GetYaxis()->SetTitleOffset(1.6); sbframe->Draw(); 
            c1->cd(2); gPad->SetLogy(1); gPad->SetLeftMargin(0.15);
            sbdataframe->GetYaxis()->SetTitleOffset(1.6); sbdataframe->Draw();
            c1->SaveAs(ZPrimeModel+"_sb_PE1_test.pdf");
        }
        // Fill per event log likelihood histogram
        RooArgSet* sbpdfobs_sb = sbpdf.getObservables(sbdata);
        RooArgSet* bpdfobs_sb = bpdf.getObservables(sbdata);
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
        double lambda_b = -2*(sbnll_b.getVal() - bnll_b.getVal());
        if (pe==0) {
            //--------
            // Draw a sample pseudoexperiment
            // Background
            RooPlot* bframe = m.frame(Title("B pdf"));
            bpdf.plotOn(bframe);
            RooPlot* bdataframe = m.frame(Title("B pdf with data"));
            bdata->plotOn(bdataframe);
            bpdf.plotOn(bdataframe);
            sbpdf.plotOn(bdataframe);
            TCanvas* c2 = new TCanvas("b_PE1","b_PE1",800,400);
            c2->Divide(2);
            c2->cd(1); gPad->SetLogy(1); gPad->SetLeftMargin(0.15); 
            bframe->GetYaxis()->SetTitleOffset(1.6); bframe->Draw();
            c2->cd(2); gPad->SetLogy(1); gPad->SetLeftMargin(0.15); 
            bdataframe->GetYaxis()->SetTitleOffset(1.6); bdataframe->Draw();
            c2->SaveAs(ZPrimeModel+"_b_PE1_test.pdf");
        }
        // Fill per event log likelihood histogram
        RooArgSet* sbpdfobs_b = sbpdf.getObservables(bdata);
        RooArgSet* bpdfobs_b = bpdf.getObservables(bdata);
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
    }
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

    c->SaveAs(ZPrimeModel+"_n2LL_test.pdf");

    //--------
    // Draw per event log likelihood ratio
    //--------
    // Signal + Background
    TCanvas *c2 = new TCanvas("c2","",900,600);
    hist_nll_event_sb->Draw("");
    hist_nll_event_sb->SetLineWidth(2);
    hist_nll_event_sb->GetXaxis()->SetTitle("-2 ln (L_{S+B} / L_{B})");
    hist_nll_event_sb->GetXaxis()->CenterTitle();

    hist_nll_event_sb->GetYaxis()->SetTitle("Events / 0.02");
    hist_nll_event_sb->GetYaxis()->CenterTitle();
    c2->SaveAs(ZPrimeModel+"_n2ll_event_sb_test.pdf");
    //--------
    // Background
    TCanvas *c3 = new TCanvas("c3","",900,600);
    hist_nll_event_b->Draw("");
    hist_nll_event_b->SetLineWidth(2);
    hist_nll_event_b->GetXaxis()->SetTitle("-2 ln (L_{S+B} / L_{B})");
    hist_nll_event_b->GetXaxis()->CenterTitle();
    hist_nll_event_b->GetYaxis()->SetTitle("Events / 0.02");
    hist_nll_event_b->GetYaxis()->CenterTitle();
    c3->SaveAs(ZPrimeModel+"_n2ll_event_b_test.pdf");



}
