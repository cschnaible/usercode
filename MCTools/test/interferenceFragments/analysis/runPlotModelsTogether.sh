#!/bin/bash


# all =  ['Q','PSI','T3L','SSM','B-L','LR','R','Y']
python PlotModelsTogether.py -in 20181026 -out 20181026 -zp all -pdf NNPDF30nlo -m 6000

for MASS in {4000,4500,5000,5500,6000,6500,7000,7500,8000}
do
    python PlotModelsTogether.py -in 20181026 -out 20181026 -zp B-L -zp Q -zp T3L -zp SSM -zp PSI -pdf NNPDF30nlo -m $MASS
done

python PlotModelsTogether.py -in 20181026 -out 20181026 -zp T3L -zp Q -zp Y -pdf NNPDF30nlo -m 6000
python PlotModelsTogether.py -in 20181026 -out 20181026 -zp T3L -zp Q -pdf NNPDF30nlo -m 6000
