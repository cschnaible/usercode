#!/bin/bash
OUT=nevents_request_alt_20181108
#python MakeInterferenceHists.py -out $OUT -id 20181010 -c 20181010 -model DY -pdf NNPDF30nlo
#python MakeInterferenceHists.py -out $OUT -id 20181001 -model DY -pdf NNPDF30nlo
#python MakeInterferenceHists.py -out $OUT -id 20181001 -model DY -pdf CT14nlo
#python MakeInterferenceHists.py -out $OUT -id 20181001 -model DY -pdf CT10nlo
#python MakeInterferenceHists.py -out $OUT -id 20180827 -model DY -pdf CTEQ5L
#
#for mass in {4000,4500,5000,5500,6000,6500,7000,7500,8000}
#do
#    for model in {ZPrimePSI,ZPrimeB-L,ZPrimeQ,ZPrimeT3L,ZPrimeSSM}
#    do
#        python MakeInterferenceHists.py -out $OUT -id 20181004 -model $model -mass $mass -pdf NNPDF30nlo
#    done
#done
#
#for pdf in {CT10nlo,CT14nlo}
#do
#    for model in {ZPrimeSSM,ZPrimeT3L}
#    do
#        python MakeInterferenceHists.py -out $OUT -id 20181010 -c 20181010 -model $model -mass 6000 -pdf $pdf
#    done
#done
#
#for pdf in {CT10nlo,CT14nlo}
#do
#    python MakeInterferenceHists.py -out $OUT -id 20181001 -model ZPrimeB-L -mass 6000 -pdf $pdf
#done
#
#for model in {ZPrimeB-L,ZPrimeSSM,ZPrimeT3L}
#do
#    for mass in {4000,6000}
#    do
#        python MakeInterferenceHists.py -out $OUT -id 20180827 -model $model -mass $mass -pdf CTEQ5L
#    done
#done
#
#for model in {ZPrimeR,ZPrimeLR,ZPrimeY}
#do 
#    python MakeInterferenceHists.py -out $OUT -id 20181010 -c 20181010 -model $model -mass 6000 -pdf NNPDF30nlo
#done
#
#for model in {ZPrimeQ,ZPrimeT3L}
#do
#    for mass in {9000,10000,11000,12000,13000}
#    do
#        python MakeInterferenceHists.py -out $OUT -c 20181010 -model $model -mass $mass -pdf NNPDF30nlo
#    done
#done
#
#for pdf in {CT10nlo,CT14nlo}
#do
#    for mass in {6000,9000}
#    do
#        python MakeInterferenceHists.py -out $OUT -id 20181010 -c 20181010 -model ZPrimeQ -mass $mass -pdf $pdf
#    done
#done

python MakeInterferenceHists.py -out $OUT -id 20181010 -c 20181010 -model DY -pdf NNPDF30nlo
python MakeInterferenceHists.py -out $OUT -id 20181004 -model ZPrimeQ -mass 6000 -pdf NNPDF30nlo
python MakeInterferenceHists.py -out $OUT -c 20181010 -model ZPrimeQ -mass 9000 -pdf NNPDF30nlo
python MakeInterferenceHists.py -out $OUT -c 20181010 -model ZPrimeQ -mass 12000 -pdf NNPDF30nlo
