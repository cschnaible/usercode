#!/bin/bash


# ZPrimeQ
for mass in {4,5,6,7,8}000
do
    python CheckNumberOfEvents.py -id 20181004 -model ZPrimeQ -mass $mass -pdf NNPDF30nlo
done
for mass in {9,10,11,12,13}000
do
    python CheckNumberOfEvents.py -id 20181010 -c 20181010 -model ZPrimeQ -mass $mass -pdf NNPDF30nlo
done

# Drell-Yan
python CheckNumberOfEvents.py -id 20181001 -model DY -pdf NNPDF30nlo
