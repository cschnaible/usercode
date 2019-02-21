#!/bin/bash
IN=inCMS_20181030
OUT=inCMS_20181030
# all =  ['Q','PSI','T3L','SSM','B-L','LR','R','Y']
#python PlotModelsTogether.py -in $IN -out $OUT -zp all -pdf NNPDF30nlo -m 6000
#
#for MASS in {4000,4500,5000,5500,6000,6500,7000,7500,8000}
#do
#    python PlotModelsTogether.py -in $IN -out $OUT -zp B-L -zp Q -zp T3L -zp SSM -zp PSI -pdf NNPDF30nlo -m $MASS
#done
#
#python PlotModelsTogether.py -in $IN -out $OUT -zp T3L -zp Q -zp Y -pdf NNPDF30nlo -m 6000
#python PlotModelsTogether.py -in $IN -out $OUT -zp T3L -zp Q -pdf NNPDF30nlo -m 6000

python PlotModelsTogether.py -in $IN -out inCMS_20181107 -zp Q -m 12000 -pdf NNPDF30nlo
