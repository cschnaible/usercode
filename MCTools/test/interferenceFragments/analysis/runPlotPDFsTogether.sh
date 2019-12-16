#!/bin/bash
IN=20190312
OUT=20190312
MASS=9000
#python PlotPDFsTogether.py -in $IN -out $OUT -zp B-L -m 4000
#python PlotPDFsTogether.py -in $IN -out $OUT -zp B-L -m 6000
#python PlotPDFsTogether.py -in $IN -out $OUT -zp SSM -m 6000
#python PlotPDFsTogether.py -in $IN -out $OUT -zp T3L -m 6000
#python PlotPDFsTogether.py -in $IN -out $OUT -zp Q -m 6000
python PlotPDFsTogether.py -in $IN -out $OUT -zp Q -m $MASS 
