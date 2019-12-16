#!/bin/bash
OUT=20190312

python MakeInterferenceHists.py -out $OUT -id 20190227 -model Q -mass 9000 -pdf NNPDF31nlo_TuneCP3
python MakeInterferenceHists.py -out $OUT -id 20190227 -model Q -mass 9000 -pdf NNPDF31nnlo_PR_TuneCP5
python MakeInterferenceHists.py -out $OUT -id 20181010 -c 20181010 -model Q -mass 9000 -pdf NNPDF30nlo
python MakeInterferenceHists.py -out $OUT -id 20181010 -c 20181010 -model Q -mass 9000 -pdf CT10nlo
python MakeInterferenceHists.py -out $OUT -id 20181010 -c 20181010 -model Q -mass 9000 -pdf CT14nlo

python MakeInterferenceHists.py -out $OUT -id 20190227 -model DY -pdf NNPDF31nlo_TuneCP3
python MakeInterferenceHists.py -out $OUT -id 20190227 -model DY -pdf NNPDF31nnlo_PR_TuneCP5
python MakeInterferenceHists.py -out $OUT -id 20181001 -model DY -pdf NNPDF30nlo
python MakeInterferenceHists.py -out $OUT -id 20181001 -model DY -pdf CT10nlo
python MakeInterferenceHists.py -out $OUT -id 20181001 -model DY -pdf CT14nlo
