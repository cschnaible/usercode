#!/bin/bash
wdir=~/www/private/ZPrime/InterferenceStudies
echo $wdir
#for mass in {4000,4500,5000,5500,6000,6500,7000,7500,8000}
#for mass in {4000,6000}
for mass in 6000
do
    for model in {Y,LR,R}
    do
        for chan in {EE,MuMu}
        do
            #for pdf in {CT10nlo,CTEQ5L,CT14nlo}
            for pdf in NNPDF30nlo
            do
                for plot in {pe_nll,pe_nll_data,event_nll}
                do
                    rm $wdir/ZPrime${model}To${chan}_ResM${mass}_Int_${pdf}_${plot}_20181017.pdf
                    cp plots/ZPrime${model}To${chan}_ResM${mass}_Int_${pdf}_${plot}_20181026.pdf $wdir
                done
            done
        done
    done
done
