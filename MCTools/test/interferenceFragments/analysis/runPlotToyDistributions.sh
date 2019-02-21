#!/bin/bash

for model in {ZPrimeQ,ZPrimeT3L}
do
    for mass in {4,5,6,7,8,9,10,11,12,13}000
    do
        python PlotToyDistributions.py -bid batch_2016_2017_20181010 -mass $mass -model $model -pdf NNPDF30nlo -out 20181027
    done
done

python PlotToyDistributions.py -bid batch_2016_2017_20181010 -mass 6000 -model ZPrimeY -pdf NNPDF30nlo -out 20181026

