void RunInterferenceHypothesisTests () {
    gROOT->ProcessLine(".L InterferenceHypothesisTest.cpp");

    std::vector<TString> models;
    models.push_back("B-L");/*models.push_back("SSM");models.push_back("T3L");
    models.push_back("LR");models.push_back("R");models.push_back("SQ");
    models.push_back("Q");models.push_back("Y");*/

    std::vector<TString> masses; 
    //masses.push_back("4000");masses.push_back("6000");
    masses.push_back("4000");masses.push_back("4500");masses.push_back("5000");
    masses.push_back("5500");masses.push_back("6000");masses.push_back("6500");
    masses.push_back("7000");masses.push_back("7500");masses.push_back("8000");

    std::vector<TString> chans; 
    chans.push_back("MuMu");//chans.push_back("EE");chans.push_back("LL");

    for (int mod = 0; mod<models.size();mod++) {
        TString model = models[mod];
        for (int ma = 0; ma<masses.size(); ma++) {
            TString mass = masses[ma];
            for (int c = 0; c<chans.size(); c++) {
                TString chan = chans[c];
                InterferenceHypothesisTest(model,chan,mass,10000,1601,600,9000,"20180923_test");
            }
        }
    }
}
