#!/bin/bash

# all = {ZPrimeQ,ZPrimeB-L,ZPrimeT3L,ZPrimePSI,ZPrimeSSM}
python PlotStatisticsVsMass.py -bid batch_2016_2017_20181010 -model all -pdf NNPDF30nlo -out 20181026
#python PlotStatisticsVsMass.py -bid batch_2016_2017_20181010 -model ZPrimeQ -pdf NNPDF30nlo -out 20181026
#python PlotStatisticsVsMass.py -bid batch_2016_2017_20181010 -model ZPrimeB-L -pdf NNPDF30nlo -out 20181026
#python PlotStatisticsVsMass.py -bid batch_2016_2017_20181010 -model ZPrimeT3L -pdf NNPDF30nlo -out 20181026
#python PlotStatisticsVsMass.py -bid batch_2016_2017_20181010 -model ZPrimeSSM -pdf NNPDF30nlo -out 20181026
