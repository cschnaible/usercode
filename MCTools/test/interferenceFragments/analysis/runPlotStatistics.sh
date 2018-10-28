#!/bin/bash

# Making all likelihood ratio comparison plots

for PDF in {CT10nlo,CT14nlo,CTEQ5L}
do
    for MODEL in {ZPrimeSSM,ZPrimeB-L,ZPrimeT3L}
    do
        for MASS in 6000
        do
            python PlotStatistics.py -bid batch_2016_2017_20181010 -model $MODEL -mass $MASS -pdf $PDF -out 20181026
        done
    done
done

# NNPDF30nlo models
for MODEL in {ZPrimeB-L,ZPrimeQ,ZPrimePSI,ZPrimeSSM,ZPrimeT3L}
do
    for MASS in {4000,4500,5000,5500,6000,6500,7000,7500,8000}
    do
        python PlotStatistics.py -bid batch_2016_2017_20181010 -model $MODEL -mass $MASS -pdf NNPDF30nlo -out 20181026
    done
done

## Remaining comparison at 6 TeV for NNPDF30nlo
for MODEL in {ZPrimeLR,ZPrimeR,ZPrimeY}
do
    python PlotStatistics.py -bid batch_2016_2017_20181010 -model $MODEL -mass 6000 -pdf NNPDF30nlo -out 20181026
done


