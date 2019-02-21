#!/bin/bash

OUT=test_20181101

python PlotRapidity.py -id 20181004 -model ZPrimeQ -mass 6000 -pdf NNPDF30nlo -out $OUT
python PlotRapidity.py -id 20181010 -c 20181010 -model ZPrimeQ -mass 9000 -pdf NNPDF30nlo -out $OUT

python PlotRapidity.py -out $OUT -id 20181010 -c 20181010 -model DY -pdf NNPDF30nlo
